"""Guidebox API calls and functions."""

import os
import requests
from model import connect_to_db, db, User, Show, StreamingService, Favorite, CableListing, Streaming, Network


GUIDEBOX_BASE_URL = "http://api-public.guidebox.com/v1.43/US/"
GUIDEBOX_API_KEY = os.environ.get('GUIDEBOX_API_KEY')

# {Base API URL} /shows/ {channel} / {limit 1} / {limit 2} / {sources} / {platform}

def guidebox_get_titles(limit_one,limit_two):
    """Searching Guidebox to get all available shows ordered by popularity.

    limit_one = where in the list of shows to start
    limit_two = how many shows to return
    """

    #create Guidebox API url
    url = GUIDEBOX_BASE_URL + GUIDEBOX_API_KEY + "/shows/all/" + limit_one + "/" + limit_two + "/all/web"

    #submit API request
    response = requests.get(url)
    #close request
    response.close()
    #save request as a json object
    response = response.json()

    # import pdb; pdb.set_trace()


    #saving just the results of the search to a variable
    show_results = response["results"]

    return show_results


def guidebox_search_title(search_word):
    """Searching Guidebox using show name."""

    #create Guidebox API url
    url = GUIDEBOX_BASE_URL + GUIDEBOX_API_KEY + "/search/title/" + search_word

    #submit API request
    response = requests.get(url)
    #close request
    response.close()
    #save request as a json object
    response = response.json()

    #saving just the results of the search to a variable to pass to jinja
    results = response["results"]

    return results

def guidebox_show_info(show_id):
    """Searching Guidebox for show information, specifically title, guidebox_id, first_aired, network, overview (description)."""

    #create Guidebox url
    show_id_url = GUIDEBOX_BASE_URL + GUIDEBOX_API_KEY + "/show/" + show_id

    #submit API request
    show_id_response = requests.get(show_id_url)
    #close request
    show_id_response.close()
    #save request as a json object
    show_info = show_id_response.json()

    return show_info

def guidebox_season_info(show_id):
    """Searching Guidebox for season information (season number and airdate) about a show."""

    #create Guidebox url
    seasons_url = GUIDEBOX_BASE_URL + GUIDEBOX_API_KEY + "/show/" + show_id + "/seasons"

    #submit API request
    seasons_response = requests.get(seasons_url)
    #close request
    seasons_response.close()
    #save request as a json object
    seasons_response = seasons_response.json()
    #save seasons_results as a variable to pass through jinja
    seasons_results = seasons_response["results"]

    return seasons_results

def guidebox_streaming_sources_info(show_id):
    """Searching Guidebox for available online streaming locations."""

    #create Guidebox url
    streaming_sources_url = GUIDEBOX_BASE_URL + GUIDEBOX_API_KEY + "/show/" + show_id + "/available_content"

    #submit API request
    streaming_sources_response = requests.get(streaming_sources_url)
    #close request
    streaming_sources_response.close()
    #save request as a json object
    streaming_sources_response = streaming_sources_response.json()

    #format response to only get web episodes 
    all_streaming_sources = streaming_sources_response["results"]["web"]["episodes"]["all_sources"]

    return all_streaming_sources


