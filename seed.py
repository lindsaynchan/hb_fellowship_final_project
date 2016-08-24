from guidebox import guidebox_get_titles, guidebox_search_title, guidebox_show_info, guidebox_season_info, guidebox_streaming_sources_info

from model import connect_to_db, db, User, Show, StreamingService, Favorite, CableListing, Streaming, Network
from server import app
from sqlalchemy import func, exc

import requests
import os
import json
GUIDEBOX_API_KEY = os.environ.get('GUIDEBOX_API_KEY')
ONCONNECT_API_KEY = os.environ.get('ONCONNECT_API_KEY')

def create_files():
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

    
    # import pdb; pdb.set_trace()


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
        
        
# def load_show_seasons():
#     """Update show objects with season information. Using the 'All Seasons in a Show" API call (guidebox_season_info())."""

#     #query database to find all the guidebox ids for all the shows in the shows table
#     guidebox_ids = db.session.query(Show.guidebox_id).all()

#     num = 1

#     #loop through each show and run individual API call for each show
#     for guidebox_object in guidebox_ids:
#         #get id attribute
#         guidebox_unicode_id = guidebox_object.guidebox_id
#         #convert unicode id to a string
#         guidebox_id = guidebox_unicode_id.encode('ascii')
#         #make API call and save result as a variable
#         result = guidebox_season_info(guidebox_id)
#         #query the database for the show object
#         show = Show.query.filter(Show.guidebox_id==guidebox_id).one()
#         #change the show's network attribute
#         show.network = result["network"]
#         print "%s has been updated in show table." % (result["title"])
#         num += 1    

#use id and search for individual show using guidebox_show_info API call: title, network, artwork, id, first aired, description
#use id and search for season info using guidebox_season_info: season number and year
#use id and search for streaming sources using guidebox_streaming_sources_info: display name

if __name__ == '__main__':
    connect_to_db(app)
    db.create_all()
    load_shows("static/show_1.txt")
    # create_files()
    # load_shows("1","250")
    # print "\n\n\n 1-250 seeded \n\n\n"
    # load_shows("251","250")
    # print "\n\n\n 251-501 seeded \n\n\n"
    # load_shows("502","250")
    # print "\n\n\n 502-752 seeded \n\n\n"
    # load_shows("753","250")
    # print "\n\n\n 753-1003 seeded \n\n\n"
    # load_shows("1004","250")
    # print "\n\n\n 1004-1254 seeded \n\n\n"
    # load_shows("1255","250")
    # print "\n\n\n 1255-1505 seeded \n\n\n"
    # load_shows("1506","250")
    # print "\n\n\n 1506-1756 seeded \n\n\n"
    # load_shows("1757","250")
    # print "\n\n\n 1757-2007 seeded \n\n\n"
    # load_shows("2008","250")
    # print "\n\n\n 2008-2258 seeded \n\n\n"
    # load_shows("2259","250")
    # print "\n\n\n 2259-2509 seeded \n\n\n"
    # load_shows("2510","250")
    # print "\n\n\n 2510-2760 seeded \n\n\n"
    # load_shows("2761","250")
    # print "\n\n\n 2761-3011 seeded \n\n\n"
    # load_shows("3012","250")
    # print "\n\n\n 3012-3262 seeded \n\n\n"
    # load_shows("3262","250")
    # print "\n\n\n 3262-3262 seeded \n\n\n"










