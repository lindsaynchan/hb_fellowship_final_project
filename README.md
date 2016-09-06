# TV Now

The shift towards watching television in non-traditional ways as well as the increase of available shows and content providers have made it harder for people to find and watch television shows that they are interested in. TV Now is a full stack web application that brings together multiple television data sources so users don't have to. Users can find and save their favorite television shows, access information about shows and locate when and where to watch them. 

___


# Technologies Used

* Python
* Javascript
* Flask
* Jinja
* JQuery
* AJAX
* Angular
* SQLAlchemy
* HTML/CSS
* Bootstrap
* PostgreSQL
* Unit and Integration Testing
* Guidebox API
* OnConnect API
* Giphy API

___


# Structure

### server.py

Core of the flask application, contains all flask routes.

### model.py

Contains tables for PostgreSQL database and example data for testing.

### guidebox.py

Contains all the functions to make Guidebox API calls.

### onconnect.py

Contains all the functions to make OnConnect API calls.

### giphy.py

Contains all the functions to make OnConnect API calls.

### seed.py

Contains methods to create seed data.

### tests.py

Contains unit and integration tests for entire app.

### favoriteslist.js and showpage.js

Contains Angular routes for user profile and show pages.


___


# Features

Search Feature

![Alt text][/static/homepage.png]

On the homepage, or from any page in the application, users can look up their favorite series using the application's search function. The search input will be encoded and used to help create an API call to Guidebox. The API call will return a list of up to 50 results at most that are exact or fuzzy matches to the original search input. 

![Alt text][/static/searchresults.png]

Once a user selects a series title from the search results displayed, a show page that is partially built using Angular will render. 

![Alt text][/static/showpage.png]

The information on the lefthand side was pulled from a database query. The information on the righthand side is broken up into 3 tabs. Since the data on this page is rendered using 5 APIs and had a long load time originally, the author decided to break up the API calls with the Angular framework. Maintaining the single, page html feel, each tab makes an AJAX call to create a database query and or create an API call to get the series information. The first tab contains information regarding the series information. The second tab contains information regarding where a series can be found online. The third tab contains information regarding where a series can be found on cable television.

If a user is logged in, a favorite's button will populate on a series' page. If a user clicks on this button, an AJAX call is made to the database, and the server will evaluate whether the user would like to add or remove the series from their favorite's list.

![Alt text][/static/userprofile.png]

If a user goes to their individual profile, they can view the list of their favorited series. Also, the user can access streaming and cable listing information regarding their favorite shows on their profile page as well. 


___

# Author

Lindsay Chan is a software engineer from San Francisco, CA.