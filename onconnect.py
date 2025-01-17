"""Guidebox API calls and functions."""

import os
import requests
from datetime import datetime, timedelta
import arrow

ONCONNECT_API_KEY = os.environ.get('ONCONNECT_API_KEY')

def onconnect_search_series_id(show_name):
    """Finding series_id using the show title name from Guidebox's information."""

    #reformatting the show name for the API call
    name = show_name.replace(" ", "+")

    #format OnConnect url
    url = "http://data.tmsapi.com/v1.1/programs/search?limit=15&q=" + name + "&entityType=series&api_key=" + ONCONNECT_API_KEY

    #submit API request
    show_search_response = requests.get(url)

    show_search_response.close()

    #save request as a json object
    show_search_response = show_search_response.json()

    #get series_id and save as a variable
    series_id = str(show_search_response["hits"][0]["program"]["seriesId"])

    return series_id

def onconnect_search_airings(onconnect_series_id):
    """Searching OnConnect TV listings for airings of the series."""

    #obtaining the current date and time in UTC
    current_date_time = datetime.now()

    #format the date time in the correct format for On Connect url
    formatted_current_date = current_date_time.strftime('%Y-%m-%d'+'T'+'%H:%M'+'Z')

    #creating URL endDate 24 hours in the future in PST
    end_date_time = current_date_time + timedelta(hours=23,minutes=59)

    #format the date time in the correct format for On Connect url
    formatted_end_date = end_date_time.strftime('%Y-%m-%d'+'T'+'%H:%M'+'Z')

    #format OnConnect url, hardcoding the lineupId (location and cable provider) and hardcoding result to PST
    url = "http://data.tmsapi.com/v1.1/series/" + onconnect_series_id + "/airings?lineupId=USA-CA04446-X&startDateTime=" + formatted_current_date + "&endDateTime=" + formatted_end_date + "&includeDetail=true&api_key=" + ONCONNECT_API_KEY

    #submit API request
    show_airings_response = requests.get(url)
    #close request
    show_airings_response.close()

    #save request as a json object
    try:
        airings_info = show_airings_response.json()
    except:
        print "\n\n\n\n\n"
        print "IN PDB!!!!"
        print "\n\n\n\n\n"
        import pdb;pdb.set_trace()

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







