from guidebox import guidebox_get_titles, guidebox_search_title, guidebox_show_info, guidebox_season_info, guidebox_streaming_sources_info

from model import connect_to_db, db, User, Show, StreamingService, Favorite, CableListing, Streaming, Network
from server import app
from sqlalchemy import func

import requests
import os
import json
GUIDEBOX_API_KEY = os.environ.get('GUIDEBOX_API_KEY')
ONCONNECT_API_KEY = os.environ.get('ONCONNECT_API_KEY')

def create_files():
    """Create txt files for data information."""

    show_info = guidebox_get_titles("1","5")

    f = open("static/show_1.txt","w")
    json.dump(show_info, f)
    f.close()

    



def load_shows():
    """Loading the Guidebox ID, show title, artwork urls and when the show first aired into the database. Using the txt results files from 'get all shows' (guidebox_get_titles()) API call."""



    #keep track of inserting rows in tables
    num = 1
    #iterate through the list of dictionaries and grab information to create show object
    for result in results:
        show = Show(guidebox_id=result["id"],
                    title=result["title"],
                    artwork_urls=[result["artwork_208x117"],
                                  result["artwork_304x171"],
                                  result["artwork_448x252"],
                                  result["artwork_608x342"]],
                    first_aired=result["first_aired"])
        db.session.add(show)
        print "%s has been added to show table." % (result["title"])
        num += 1
    db.session.commit()
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
    # connect_to_db(app)
    # db.create_all()
    create_files()
    # load_shows()
    # load_show_network_description()
