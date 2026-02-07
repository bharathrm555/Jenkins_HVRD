# test_app.py
import unittest
from app import app

class FlaskTestCase(unittest.TestCase):
    
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
    
    def test_home_status_code(self):
        """Test if home page returns 200"""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        print("✓ Home page test passed")
    
    def test_home_content(self):
        """Test home page content"""
        response = self.app.get('/')
        self.assertIn(b'Flask Application Deployed', response.data)
        print("✓ Home content test passed")
    
    def test_health_endpoint(self):
        """Test health endpoint"""
        response = self.app.get('/health')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'healthy', response.data)
        print("✓ Health endpoint test passed")
    
    def test_student_endpoint(self):
        """Test student info endpoint"""
        response = self.app.get('/student')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Bharath', response.data)
        print("✓ Student endpoint test passed")

if __name__ == '__main__':
    print("=" * 50)
    print("Running Flask Application Tests")
    print("=" * 50)
    unittest.main(verbosity=2)