"""
Unit tests for the Personal Portfolio app.

Uses unittest and Flask's test client to verify public and admin functionalities.
"""

import os
import tempfile
import unittest
from app import create_app, db

class PortfolioTestCase(unittest.TestCase):
    def setUp(self):
        """
        Set up a temporary Flask application and database for testing.
        """
        self.db_fd, self.db_path = tempfile.mkstemp()
        test_config = {
            'TESTING': True,
            'DATABASE': self.db_path,
            'SECRET_KEY': 'test',
            'ADMIN_USERNAME': 'admin',
            'ADMIN_PASSWORD': 'password'
        }
        self.app = create_app(test_config)
        self.client = self.app.test_client()
        
        with self.app.app_context():
            db.init_db()
            # Insert a sample project
            db.get_db().execute(
                "INSERT INTO projects (title, description, link) VALUES (?, ?, ?)",
                ("Test Project", "Description of test project", "https://example.com")
            )
            # Insert a sample blog post
            db.get_db().execute(
                "INSERT INTO blog_posts (title, content) VALUES (?, ?)",
                ("Test Blog", "Content of test blog post")
            )
            db.get_db().commit()

    def tearDown(self):
        """
        Remove temporary database.
        """
        os.close(self.db_fd)
        os.unlink(self.db_path)

    def test_homepage(self):
        """
        Test that the homepage loads and displays sample content.
        """
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Welcome to My Portfolio", response.data)
        self.assertIn(b"Test Project", response.data)
        self.assertIn(b"Test Blog", response.data)

    def test_project_detail(self):
        """
        Test that a project detail page loads.
        """
        with self.app.app_context():
            project = db.get_db().execute("SELECT id FROM projects WHERE title = ?", ("Test Project",)).fetchone()
            project_id = project['id']
        response = self.client.get(f'/project/{project_id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Description of test project", response.data)

    def test_blog_detail(self):
        """
        Test that a blog post detail page loads.
        """
        with self.app.app_context():
            post = db.get_db().execute("SELECT id FROM blog_posts WHERE title = ?", ("Test Blog",)).fetchone()
            post_id = post['id']
        response = self.client.get(f'/blog/{post_id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Content of test blog post", response.data)

    def test_admin_login_logout(self):
        """
        Test admin login and logout functionality.
        """
        # Test login with incorrect credentials
        response = self.client.post('/login', data={'username': 'wrong', 'password': 'wrong'}, follow_redirects=True)
        self.assertIn(b"Invalid username or password", response.data)
        # Login with correct credentials
        response = self.client.post('/login', data={'username': 'admin', 'password': 'password'}, follow_redirects=True)
        self.assertIn(b"Logged in successfully", response.data)
        # Logout
        response = self.client.get('/logout', follow_redirects=True)
        self.assertIn(b"Logged out successfully", response.data)

if __name__ == '__main__':
    unittest.main()
