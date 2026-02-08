# Simple Test File
import unittest
from app import app

class SimpleFlaskTests(unittest.TestCase):
    
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
    
    def test_home_page(self):
        """Test if home page loads"""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Jenkins CI/CD Pipeline', response.data)
        print("✓ Home page test passed")
    
    def test_health_endpoint(self):
        """Test health endpoint"""
        response = self.app.get('/health')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'healthy', response.data)
        print("✓ Health endpoint test passed")
    
    def test_info_endpoint(self):
        """Test info endpoint"""
        response = self.app.get('/info')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'student', response.data)
        print("✓ Info endpoint test passed")
    
    def test_test_endpoint(self):
        """Test test endpoint"""
        response = self.app.get('/test')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'successful', response.data)
        print("✓ Test endpoint test passed")

if __name__ == '__main__':
    print("\n" + "="*50)
    print("Running Flask Application Tests")
    print("="*50)
    unittest.main(verbosity=2)
    print("="*50)
    print("All tests completed!")
    print("="*50)