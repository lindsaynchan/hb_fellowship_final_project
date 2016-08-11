"""Television listings and streaming search."""

import os
from jinja2 import StrictUndefined
from flask import Flask, render_template, request, flash, redirect, session
from model import connect_to_db, db, User, Show, StreamingService, Favorite, CableListing, Streaming, Network
from urllib import urlencode
import requests

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
    #triple url code search
        # encoded_search = urlencode(search)
        # print encoded_search
    #turn unicode into string
    #create Guidebox API url
        # url = GUIDEBOX_BASE_URL + GUIDEBOX_API_KEY + "/search/title/" + encoded_search

    url = GUIDEBOX_BASE_URL + GUIDEBOX_API_KEY + "/search/title/Arrested"

    #submit API request
    response = requests.get(url)
    response.close()
    #save request as a json object
    response = response.json()

    #saving just the results of the search to a variable to pass to jinja
    results = response["results"]

    return render_template("search_results.html", results=results)

@app.route('/show/<guidebox_id>')
def series_information(guidebox_id):
    """Show page."""

    #using title to get API information from Guidebox


    return render_template("show_page.html")

# @app.route('/user/<user_id>')
# def index(user_id):
#     """Show user's profile."""

#     return render_template("show_profile.html")


##########################################################################

if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0")

