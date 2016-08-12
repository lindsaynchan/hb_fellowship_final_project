"""Guidebox API calls and functions."""

import os
import requests
from datetime import datetime, timedelta

ONCONNECT_API_KEY = os.environ.get('ONCONNECT_API_KEY')

def onconnect_search_series_id(show_name):
    """Finding series_id using the show title name from Guidebox's information."""

    name = show_name.replace(" ", "+")

    print show_name

    #format OnConnect url
    url = "http://data.tmsapi.com/v1.1/programs/search?limit=1&q=" + name + "&entityType=series&api_key=" + ONCONNECT_API_KEY

    print url

    #submit API request
    show_search_response = requests.get(url)
    #close request

    show_search_response.close()
    #save request as a json object

    show_search_response = show_search_response.json()

    print show_search_response

    #get series_id and save as a variable
    series_id = str(show_search_response["hits"][0]["program"]["seriesId"])

    print series_id

    return series_id

def onconnect_search_airings(onconnect_series_id):
    """Searching OnConnect TV listings for airings of the series."""

    #obtaining the current date and time at the moment
    current_date_time = datetime.now()
    #creating end date 24 hours in the future
    full_day = current_date_time + timedelta(hours=23,minutes=59)

    #format the date time in the correct format for On Connect url
    formatted_current_date_time = current_date_time.strftime('%Y-%m-%d'+'T'+'%H:%M'+'Z')
    #format the date time in the correct format for On Connect url
    formatted_full_day = full_day.strftime('%Y-%m-%d'+'T'+'%H:%M'+'Z')

    #format OnConnect url, hardcoding the lineupId (location and cable provider)
    url = "http://data.tmsapi.com/v1.1/series/" + onconnect_series_id + "/airings?lineupId=USA-CA04446-X&startDateTime=" + formatted_current_date_time + "&endDateTime=" + formatted_full_day + "&includeDetail=true&api_key=" + ONCONNECT_API_KEY

    #submit API request
    show_airings_response = requests.get(url)
    #close request
    show_airings_response.close()
    #save request as a json object
    airings_info = show_airings_response.json()

    print airings_info    

    return airings_info







