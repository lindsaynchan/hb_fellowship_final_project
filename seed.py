from guidebox import guidebox_get_titles, guidebox_search_title, guidebox_show_info, guidebox_season_info, guidebox_streaming_sources_info

from model import connect_to_db, db, User, Show, StreamingService, Favorite, CableListing, Streaming, Network
from onconnect import onconnect_search_series_id
from server import app
from sqlalchemy import func, exc

import requests
import os
import json
import arrow
import time

GUIDEBOX_API_KEY = os.environ.get('GUIDEBOX_API_KEY')
ONCONNECT_API_KEY = os.environ.get('ONCONNECT_API_KEY')

def create_guidebox_files():
    """Create txt files for data information."""

    # need to get data in one txt file for results 1-19800

    #set the limit of the results, can only get results from 1-250
    a = 1
    b = 250
    shows = []

    #19801
    while a < 20053:
        shows_info = guidebox_get_titles(str(a),str(b))
        shows.extend(shows_info)

        a = a + b
        

    f = open("static/show_2_v2.txt","w")
    json.dump(shows, f)
    f.close()

# TO GET THE TXT FILE BACK
# import json
# from pprint import pprint

# with open('data.json') as data_file:    
#     data = json.load(data_file)

# pprint(data)


def load_shows(data_file):
    """Loading the Guidebox ID, show title, artwork urls and when the show first aired into the database. Using the txt results files from 'get all shows' (guidebox_get_titles()) API call."""

    f = open(data_file)
    results = json.load(f)

    #keep track of inserting rows in tables
    num = 1
    #iterate through the list of dictionaries and grab information to create show object
    for result in results:
        if result["first_aired"]:
            try:
                show = Show(guidebox_id=result["id"],
                            title=result["title"],
                            artwork_urls=result["artwork_608x342"],
                            first_aired=result["first_aired"])
                db.session.add(show)
                print "%s has been added to show table." % (result["title"])
                num += 1
                db.session.commit()
            except exc.IntegrityError as e:
                db.session.rollback()
                print "Duplicate entry: %s" % e
        else:
            try:
                show = Show(guidebox_id=result["id"],
                            title=result["title"],
                            artwork_urls=result["artwork_608x342"])
                db.session.add(show)
                print "%s has been added to show table." % (result["title"])
                num += 1
                db.session.commit()
            except exc.IntegrityError as e:
                db.session.rollback()
                print "Duplicate entry: %s" % e


def load_show_network_description():
    """Update show objects with network and description information. Using the 'get basic show info' API call (guidebox_show_info())."""

    #query database to find all the guidebox ids for all the shows in the shows table
    guidebox_ids = db.session.query(Show.guidebox_id).all()

    num = 1

    #loop through each show and run individual API call for each show
    for guidebox_object in guidebox_ids:
        #get id attribute
        guidebox_unicode_id = guidebox_object.guidebox_id
        #convert unicode id to a string
        guidebox_id = guidebox_unicode_id.encode('ascii')
        #make API call and save result as a variable
        result = guidebox_show_info(guidebox_id)
        #query the database for the show object
        show = Show.query.filter(Show.guidebox_id==guidebox_id).one()
        #change the show's network attribute
        show.network = result["network"]
        #change the show's description attribute
        show.description = result["overview"]
        print "%s has been updated in show table." % (result["title"])
        num += 1
    
    db.session.commit()
        
        
def load_show_seasons():
    """Update show objects with season information. Using the 'All Seasons in a Show" API call (guidebox_season_info())."""

    #query database to find all the guidebox ids for all the shows in the shows table
    guidebox_ids = db.session.query(Show.guidebox_id).all()

    num = 1

    #loop through each show and run individual API call for each show
    for guidebox_object in guidebox_ids:
        #get id attribute
        guidebox_unicode_id = guidebox_object.guidebox_id
        #convert unicode id to a string
        guidebox_id = guidebox_unicode_id.encode('ascii')
        #make API call and save result as a variable
        result = guidebox_season_info(guidebox_id)
        #query the database for the show object
        show = Show.query.filter(Show.guidebox_id==guidebox_id).one()
        #change the show's network attribute
        show.network = result["network"]
        print "%s has been updated in show table." % (result["title"])
        num += 1    

def onconnect_tv_listings(series_id):

    url = "http://data.tmsapi.com/v1.1/series/" + series_id + "/airings?lineupId=USA-CA04446-X&startDateTime=2016-09-10T10:00Z&endDateTime=2016-09-11T9:59Z&includeDetail=true&api_key=" + ONCONNECT_API_KEY

    #submit API request
    show_airings_response = requests.get(url)
    #close request
    show_airings_response.close()

    #save request as a json object
    airings_info = show_airings_response.json()

    #loop through each airing and change and replace the datetime string with arrow library and putting it into PST
    for airing in airings_info:
        start_time = airing["startTime"]
        start_time = start_time.replace("T", "")
        start_time = start_time.replace("Z", "")
        arrow_time = arrow.get(start_time, 'YYYY-MM-DDHH:mm').replace(hours=-7)
        arrow_time = arrow_time.format('h:mma ddd MMM DD, YYYY')
        #format a = am/pm, h = none army time for hours
        airing["startTime"] = arrow_time

    return airings_info


def create_onconnect_files():
    """Grab TV Listings Information for Demo."""

    shows = ["Modern Family", "American Dad!", "American Horror Story", "Game of Thrones", "House of Cards", "The Bachelor", "The Simpsons"]

    tv_listings = []

    for show in shows:
        show_info = {}
        series_id = onconnect_search_series_id(show)
        airings_info = onconnect_tv_listings(series_id)
        
        show_info["title"] = show
        if airings_info:
            show_info["listings"] = airings_info
        else:
            show_info["listings"] = ["empty"]

        tv_listings.append(show_info)
        print "Added %s to list." % show
        time.sleep(1)

    f = open("static/series_listings.txt","w")
    json.dump(tv_listings, f)
    f.close()


def load_listings(data_file):
    """Load listings information in database."""

    f = open(data_file)
    results = json.load(f)

    #keep track of inserting rows in tables
    num = 1
    #iterate through the list of dictionaries and grab information to create show object
    for show in shows:
        
        if result["first_aired"]:
            try:
                show = Show(guidebox_id=result["id"],
                            title=result["title"],
                            artwork_urls=result["artwork_608x342"],
                            first_aired=result["first_aired"])
                db.session.add(show)
                print "%s has been added to show table." % (result["title"])
                num += 1
                db.session.commit()
            except exc.IntegrityError as e:
                db.session.rollback()
                print "Duplicate entry: %s" % e
        else:
            try:
                show = Show(guidebox_id=result["id"],
                            title=result["title"],
                            artwork_urls=result["artwork_608x342"])
                db.session.add(show)
                print "%s has been added to show table." % (result["title"])
                num += 1
                db.session.commit()
            except exc.IntegrityError as e:
                db.session.rollback()
                print "Duplicate entry: %s" % e

#########################################################################

if __name__ == '__main__':
    connect_to_db(app)
    db.create_all()
    load_shows("/static/show_1.txt")
    # load_listings("/static/series_listings.txt")










