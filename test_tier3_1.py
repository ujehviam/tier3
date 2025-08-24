import unittest
import models
import services
import os

TEST_DB = "test_app.db"

class TestServices(unittest.TestCase):

    def setUp(self):
        """Run before each test - create a fresh test DB"""
        if os.path.exists(TEST_DB):
            os.remove(TEST_DB)
        models.Tier3 = TEST_DB   # switch DB to test version
        models.init_db()

    def tearDown(self):
        """Run after each test - cleanup"""
        if os.path.exists(TEST_DB):
            os.remove(TEST_DB)

    def test_register_user(self):
        """Test user registration"""
        success, msg = services.register_user("alice", "password123")
        self.assertTrue(success)
        self.assertEqual(msg, "User registered successfully!")

        # Try duplicate registration
        success, msg = services.register_user("alice", "password123")
        self.assertFalse(success)
        self.assertIn("Error", msg)

    def test_authenticate_user(self):
        """Test login functionality"""
        services.register_user("bob", "mypassword")

        # Correct credentials
        self.assertTrue(services.authenticate_user("bob", "mypassword"))

        # Wrong password
        self.assertFalse(services.authenticate_user("bob", "wrongpass"))

        # Non-existent user
        self.assertFalse(services.authenticate_user("ghost", "nope"))

    def test_get_all_users(self):
        """Test listing users"""
        services.register_user("charlie", "abc123")
        services.register_user("david", "xyz789")

        users = services.get_all_users()
        self.assertIn("charlie", users)
        self.assertIn("david", users)
        self.assertEqual(len(users), 2)


if __name__ == "__main__":
    unittest.main()