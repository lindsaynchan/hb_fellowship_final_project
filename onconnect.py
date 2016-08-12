"""Guidebox API calls and functions."""

import os
import requests
import datetime

ONCONNECT_API_KEY = os.environ.get('ONCONNECT_API_KEY')

def onconnect_search_series_id(show_name):
    """Finding series_id using the show title name from Guidebox's information."""
    
    name = show_name(" ", "+")

    #format OnConnect url
    url = "http://data.tmsapi.com/v1.1/programs/search?q=" + name + "&entityType=series&api_key=" + ONCONNECT_API_KEY

    #submit API request
    show_search_response = requests.get(url)
    #close request
    show_search_response.close()
    #save request as a json object
    show_search_response = response.json()

    #get series_id and save as a variable
    series_id = str(show_search_response["hits"][0]["program"]["seriesId"])

    return series_id

def onconnect_search_airings(onconnect_series_id):
    """Searching OnConnect TV listings for airings of the series."""

    #format OnConnect url, hardcoding the lineupId (location and cable provider)
    url = "http://data.tmsapi.com/v1.1/series/" + onconnect_series_id + "/airings?lineupId=USA-CA04446-X&startDateTime=" + 2015-02-14T10:00Z&includeDetail=true&api_key=1234567890

    url = "http://data.tmsapi.com/v1.1/programs/search?q=" + name + "&entityType=series&api_key=" + ONCONNECT_API_KEY

    #submit API request
    show_search_response = requests.get(url)
    #close request
    show_search_response.close()
    #save request as a json object
    show_search_response = response.json()    









