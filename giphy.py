"""Giphy API calls and functions."""

import os
import requests

GIPHY_API_KEY = os.environ.get('GIPHY_API_KEY')

def giphy_random_generator():
    """Generate random television related gif."""

    url = "http://api.giphy.com/v1/gifs/random?api_key=" + GIPHY_API_KEY + "&rating=pg&tag=television"

    #submit API request
    gif = requests.get(url)

    gif.close()

    #save request as a json object
    gif = gif.json()

    gif_url = gif["data"]["image_url"]

    return gif_url