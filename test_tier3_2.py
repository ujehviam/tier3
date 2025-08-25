import unittest
import os
import models
from app import app

TEST_DB = "test_app.db"

class TestFlaskApp(unittest.TestCase):

    def setUp(self):
        """Setup test environment before each test"""
        # Use a fresh DB
        if os.path.exists(TEST_DB):
            os.remove(TEST_DB)
        models.Tier3 = TEST_DB
        models.init_db()

        # Setup Flask test client
        self.app = app.test_client()
        self.app.testing = True

    def tearDown(self):
        """Cleanup after each test"""
        if os.path.exists(TEST_DB):
            os.remove(TEST_DB)

    def test_register_route(self):
        """Test registering a new user"""
        response = self.app.post("/register", data=dict(
            username="alice",
            password="password123"
        ), follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Login", response.data)  # after register, should redirect to login page

    def test_login_route(self):
        """Test login with valid and invalid credentials"""
        # First, register user
        self.app.post("/register", data=dict(
            username="bob",
            password="mypassword"
        ), follow_redirects=True)

        # Correct login
        response = self.app.post("/login", data=dict(
            username="bob",
            passwor="mypassword"
        ), follow_redirects=True)
        self.assertIn(b"Welcome, bob", response.data)

        # Wrong password
        response = self.app.post("/login", data=dict(
            username="bob",
            password="wrongpass"
        ), follow_redirects=True)
        self.assertIn(b"Invalid credentials", response.data)

    def test_logout_route(self):
        """Test logout after login"""
        # Register and login first
        self.app.post("/register", data=dict(
            username="charlie",
            password="secret"
        ), follow_redirects=True)
        self.app.post("/login", data=dict(
            username="charlie",
            password="secret"
        ), follow_redirects=True)

        # Now logout
        response = self.app.get("/logout", follow_redirects=True)
        self.assertIn(b"Login", response.data)  # should redirect to login page


if __name__ == "__main__":
    unittest.main()