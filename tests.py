from unittest import TestCase
from model import connect_to_db, db, User, Show, StreamingService, Favorite, CableListing, Streaming, Network, example_data
from server import app
import server
import json



class BasicFlaskTests(TestCase):
    """Flask tests."""

    def setUp(self):
        """Set up before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        """Test homepage."""

        result = self.client.get("/")
        self.assertIn("Find your favorite show!", result.data)

    def test_no_search_results(self):
        """Test search no results for search results page."""

        result = self.client.get("/search-results")
        self.assertIn("Sorry, there's nothing that matches your search!", result.data)

    def test_search_results(self):
        """Test search results page."""

        result = self.client.get("/search-results?search=america")
        self.assertIn("America", result.data)

    def test_login_page(self):
        """Test login page."""

        result = self.client.get('/login')
        self.assertIn("Email:", result.data)

    def test_new_user_page(self):
        """Test new user page."""

        result = self.client.get('/new-user')
        self.assertIn("New User", result.data)

class TestsUserClassMethodsDatabase(TestCase):
    """Tests the user class methods that use the database."""

    def setUp(self):
        """Set up before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

        connect_to_db(app, "postgresql:///testdb")
        db.create_all()
        example_data()

    def tearDown(self):
        """Tear down after every test."""

        db.session.close()
        db.drop_all()

    def test_user_email_query(self):
        """Test finding user in database with email."""
        
        user = User.get_user_with_email("hello@hello.com")
        self.assertEqual("hello@hello.com", user.email)

    def test_add_user(self):
        """Test adding user to database."""

        User.add_user("hi@hello.com", "hi")
        user = User.query.filter(User.email=='hi@hello.com').one()
        self.assertEqual("hi@hello.com", user.email)

    def test_find_user_id_with_email(self):
        """Test finding user id in database with email."""

        user = User.find_user_id_with_email("hello@hello.com")
        self.assertEqual(1, user.user_id)


class TestsShowClassMethodsDatabase(TestCase):
    """Tests the show class methods that use the database."""

    def setUp(self):
        """Set up before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

        connect_to_db(app, "postgresql:///testdb")
        db.create_all()
        example_data()

    def tearDown(self):
        """Tear down after every test."""

        db.session.close()
        db.drop_all()

    def test_find_show_with_guidebox_id(self):
        """Test query of finding show with guidebox id."""

        show = Show.find_show_with_guidebox_id("169")
        self.assertEqual("Modern Family", show.title)

    def test_add_show(self):
        """Test adding show to database."""

        friends = unicode("Friends","utf-8")
        description = unicode("Six young people, on their own and struggling to survive in the real world, find the companionship, comfort and support they get from each other to be the perfect antidote to the pressures of life.", "utf-8")

        show_info = {"id":"29","title":friends,"artwork_608x342":"http://static-api.guidebox.com/thumbnails_xlarge/1737-2397346851-608x342.jpg","first_aired":"1994-09-22","overview":description}


        Show.add_show(show_info)
        show = Show.query.filter(Show.title=="Friends").one()
        self.assertEqual("Friends", show.title)

    def test_add_description_network_to_show(self):
        """Test adding description and network to a show in the database."""

        description = unicode("Seven noble families fight for control of the mythical land of Westeros.","utf-8")
        show = Show.query.filter(Show.title=="Game of Thrones").one()
        show_data = {"overview":description,"network":"HBO"}

        Show.add_description_network_to_show(show, show_data)
        show = Show.query.filter(Show.title=="Game of Thrones").one()
        self.assertEqual("HBO", show.network)

    def test_as_dict(self):
        """Test dictionary conversion."""

        show = Show.query.filter(Show.title=="Game of Thrones").one()
        dictionary = show.as_dict()
        self.assertIn("guidebox_id", dictionary)


class TestsFavoriteClassMethodsDatabase(TestCase):
    """Tests the favorite class methods that use the database."""

    def setUp(self):
        """Set up before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

        connect_to_db(app, "postgresql:///testdb")
        db.create_all()
        example_data()

    def tearDown(self):
        """Tear down after every test."""

        db.session.close()
        db.drop_all()

    def test_find_show_favorites_list(self):
        """Test find show in favorites list method."""

        favorites = Favorite.find_show_favorites_list("67", "1")
        self.assertEqual("67", favorites[0].guidebox_id)

    def test_add_to_favorites(self):
        """Test add show to user's favorites list."""

        Favorite.add_to_favorites("6959", "1")
        favorite = Favorite.query.filter(Favorite.guidebox_id=="6959", Favorite.user_id=="1").one()
        self.assertEqual("6959", favorite.guidebox_id)

    def test_delete_favorite(self):
        """Test deleting favorite from database."""

        Favorite.delete_favorite("67")
        favorites = Favorite.query.filter(Favorite.user_id=="1").all()
        favorite_ids = []
        for favorite in favorites:
            favorite_ids.append(favorite.guidebox_id)
        self.assertNotIn("67",favorite_ids)


class FlaskTestsDatabase(TestCase):
    """Flask tests that use the database."""

    def setUp(self):
        """Set up before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

        connect_to_db(app, "postgresql:///testdb")
        db.create_all()
        example_data()

    def tearDown(self):
        """Tear down after every test."""

        db.session.close()
        db.drop_all()

    def test_login(self):
        """Test login function."""

        result = self.client.post("/login-user",
                                  data={"email":"hello@hello.com", "password":"hello"},
                                  follow_redirects=True)
        self.assertIn("Logged in as", result.data)

    def test_login_fail(self):
        """Test login function if user not in database."""

        result = self.client.post("/login-user",
                                  data={"email":"hi@hello.com", "password":"hello"},
                                  follow_redirects=True)
        self.assertIn("That email is not", result.data)

    def test_login_wrong_password(self):
        """Test login function if wrong password was entered."""

        result = self.client.post("/login-user",
                                  data={"email":"hello@hello.com", "password":"hi"},
                                  follow_redirects=True)
        self.assertIn("That email and password", result.data)

    def test_user_in_system_already(self):
        """Test if system prevents user from entering duplicate email."""

        result = self.client.post('/create-new-user',
                                  data={"email":"hello@hello.com","password":"hello"},
                                  follow_redirects=True)
        self.assertIn("That email is already", result.data)

    def test_add_new_user(self):
        """Test adding new user in the system."""

        result = self.client.post('/create-new-user',
                                  data={"email":"hi@hello.com","password":"hello"},
                                  follow_redirects=True)
        self.assertIn("Login", result.data)

    def test_show_page(self):
        """Test show page."""

        result = self.client.get("/show/169")
        self.assertIn("Modern Family", result.data)

    def test_show_info(self):
        """Test show info section on show page."""

        result = self.client.get("/show/169/show_info")
        self.assertIn("Network", result.data)
        self.assertIn("Seasons", result.data)

class FlaskTestsLoggedIn(TestCase):
    """Flask tests with user logged in to session."""

    def setUp(self):
        """Set up before every test."""

        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'key'
        self.client = app.test_client()

        with self.client as c:
            with c.session_transaction() as sess:
                sess['current_user'] = "hello@hello.com"

        connect_to_db(app, "postgresql:///testdb")
        db.create_all()
        example_data()

    def tearDown(self):
        """Tear down after every test."""

        db.session.close()
        db.drop_all()

    def test_homepage_logged_in(self):
        """Test homepage buttons are correct if user is logged in."""

        result = self.client.get("/")
        self.assertIn("Profile",result.data)

    def test_logout(self):
        """Test logout button/route functionality."""

        result = self.client.get('/logout', follow_redirects=True)
        self.assertIn("Logged out", result.data)

    def test_favorites_button_on_show_page(self):
        """Test if favorites button is located on show page while logged in."""

        result = self.client.get("/show/169")
        self.assertIn("Modern Family", result.data)
        self.assertIn("Favorite", result.data)


####################################################################

if __name__ == '__main__':
    import unittest

    unittest.main()













