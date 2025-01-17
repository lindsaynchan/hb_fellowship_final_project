# TV Now


Learn more about the developer: https://www.linkedin.com/in/lindsaynchan


The shift towards watching television in non-traditional ways as well as the increase of available shows and content providers have made it harder for people to find and watch television shows that they are interested in. TV Now is a full stack web application that brings together multiple television data sources so users don't have to. Users can find and save their favorite television shows, access information about shows and locate when and where to watch them. 


___



# Technologies Used

* Python
* Javascript
* Flask
* Jinja
* JQuery
* AJAX
* AngularJS
* SQLAlchemy
* HTML/CSS
* Bootstrap
* PostgreSQL
* Python Unittest Module
* Guidebox API
* OnConnect API
* Giphy API


___



# Structure

#### server.py

Core of the flask application, contains all flask routes.

#### model.py

Contains tables for PostgreSQL database and example data for testing.

#### guidebox.py

Contains all the functions to make Guidebox API calls.

#### onconnect.py

Contains all the functions to make OnConnect API calls.

#### giphy.py

Contains all the functions to make Giphy API calls.

#### seed.py

Contains methods to create seed data.

#### tests.py

Contains unit and integration tests for entire app.

#### static directory

Contains .js files that contain AngularJS routes for user profile and show pages, seed data files, html pages that use AngularJS, and image files.

#### templates directory

Contains the html files that do not use AngularJS.

___



# Features

### Search Feature


![alt text](/static/homepage.png)


On the homepage, or from any page in the application, users can look up their favorite series using the application's search function. The search input will be encoded and used to help create an API call to Guidebox. The API call will return a list of up to 50 results that are exact or fuzzy matches to the original search input. 


![alt text](/static/searchresults.png)


Once a user selects a series title from the search results displayed, a show page that is built using AngularJS will render. 


### Show Page


![alt text](/static/showpage.png)


The information displayed on the lefthand side is pulled from a database query. The information displayed on the righthand side is broken up into 3 tabs. 

### Decreasing Load Time
Since the data on the entire page is rendered using 5 API calls, the page originally had a long load time. To cut down the load time, the page was altered to break up the API calls using AngularJS. This architecture decision maintains a single page html feel. When selected, each tab makes an AJAX call to either query the database or make an API call to get the series' information. The first tab contains information regarding the series information, the second tab contains information regarding where a series can be found online and the third tab contains information regarding where a series can be found on cable television.

### Dynamic User Interface

If a user is logged in, a favorite button will populate on the show page. If a user clicks on this button, an AJAX call is made to the database, and the server will evaluate whether the user would like to add or remove the series from their favorites list.


![alt text](/static/userprofile.png)
 

If a user goes to their individual profile, they can view the list of their favorited series. The user can access streaming and cable listing information regarding all their favorite shows on their profile page as well. 


___



# Author

Lindsay Chan is a software engineer from San Francisco, CA.
