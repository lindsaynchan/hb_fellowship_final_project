"""Television listings and streaming search."""

import os
from jinja2 import StrictUndefined
from flask import Flask, render_template, request, flash, redirect, session
from model import connect_to_db, db, User, Show, StreamingService, Favorite, CableListing, Streaming, Network
import requests
import urllib2

GUIDEBOX_BASE_URL = "http://api-public.guidebox.com/v1.43/US/"

app = Flask(__name__)

app.secret_key = os.environ.get('APP_KEY')
GUIDEBOX_API_KEY = os.environ.get('GUIDEBOX_API_KEY')
ONCONNECT_API_KEY = os.environ.get('ONCONNECT_API_KEY')

app.jinja_env.undefined = StrictUndefined

##########################################################################

#creating homepage route to return homepage.html
@app.route('/')
def show_index():
    """Homepage."""

    return render_template("homepage.html")

#creating search results route that will show series results from Guidebox API 
#call
@app.route('/search-results')
def show_results():
    """Search results page."""

    #get the search bar input and save as a variable
    search = request.args.get("search")
    #turn unicode in string
    search = str(search)
    #encode search
    encoded_search = urllib2.quote(search)

    #create Guidebox API url
    url = GUIDEBOX_BASE_URL + GUIDEBOX_API_KEY + "/search/title/" + encoded_search


    #submit API request
    response = requests.get(url)
    #close request
    response.close()
    #save request as a json object
    response = response.json()

    #saving just the results of the search to a variable to pass to jinja
    results = response["results"]

    return render_template("search_results.html", results=results)

@app.route('/show/<guidebox_id>')
def series_information(guidebox_id):
    """Show page."""

    #using guidebox_id to get API information from Guidebox

    #{Base API URL} /show/ {id} - title, guidebox_id, first_aired, network, overview
    show_id_url = GUIDEBOX_BASE_URL + GUIDEBOX_API_KEY + "/show/" + guidebox_id

    #submit API request
    show_id_response = requests.get(show_id_url)
    #close request
    show_id_response.close()
    #save request as a json object
    show_info = show_id_response.json()


    #{Base API URL} /show/ {id} /seasons - season # and first airdate (get year)
    seasons_url = GUIDEBOX_BASE_URL + GUIDEBOX_API_KEY + "/show/" + guidebox_id + "/seasons"

    #submit API request
    seasons_response = requests.get(seasons_url)
    #close request
    seasons_response.close()
    #save request as a json object
    seasons_response = seasons_response.json()
    #save seasons_results as a variable to pass through jinja
    seasons_results = seasons_response["results"]

    #{Base API URL} /show/ {id} /available_content - get streaming sources

    streaming_sources_url = GUIDEBOX_BASE_URL + GUIDEBOX_API_KEY + "/show/" + guidebox_id + "/available_content"

    #submit API request
    streaming_sources_response = requests.get(streaming_sources_url)
    #close request
    streaming_sources_response.close()
    #save request as a json object
    streaming_sources_response = streaming_sources_response.json()

    #format response to only get web episodes 
    all_streaming_sources = streaming_sources_response["results"]["web"]["episodes"]["all_sources"]

    #get title for OnConnect API call
    #format the OnConnect API call to get series_id
    #save series id to variable
    #format the OnConnect API call to get schedule data

    return render_template("show_page.html",
                            show_info=show_info, 
                            seasons_results=seasons_results,
                            all_streaming_sources=all_streaming_sources)

# @app.route('/user/<user_id>')
# def index(user_id):
#     """Show user's profile."""

#     return render_template("show_profile.html")


##########################################################################

if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0")

