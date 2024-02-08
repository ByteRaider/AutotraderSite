from django.urls import reverse
from django.test import TestCase
from django.contrib.auth.models import User

class UserAccountTests(TestCase):

    def test_user_registration(self):
        # Define the registration URL
        registration_url = reverse('register')
        # Define registration data
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'complex_password',
            'password2': 'complex_password',  # Confirmation password
        }
        # Send a POST request to the registration URL
        response = self.client.post(registration_url, data)
        
        # Check that the user was created
        self.assertEqual(User.objects.count(), 1)
        # Check that the response redirected to the correct page (e.g., home or login)
        self.assertRedirects(response, reverse('login'))  # Adjust as necessary

    def test_user_login(self):
        # Create a user
        User.objects.create_user(username='testuser', password='complex_password')
        # Define the login URL
        login_url = reverse('login')
        # Define login credentials
        data = {
            'username': 'testuser',
            'password': 'complex_password',
        }
        # Send a POST request to the login URL
        response = self.client.post(login_url, data)
    
        # Check for successful redirect after login, typically to the home page or user's profile page
        self.assertRedirects(response, expected_url=reverse('profile'), status_code=302, target_status_code=200)
    
        # Alternatively, check if the test client is authenticated by attempting to access a page that requires authentication
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)  # Adjust the status code and URL as necessary


    def test_logout(self):
        # Log in the user
        self.client.login(username=self.username, password=self.password)
        
        # Log out the user using POST
        response = self.client.post(reverse('logout'), follow=True)
        
        # Check that the response redirects to the login page (or your chosen next_page)
        self.assertRedirects(response, reverse('login'), status_code=302, target_status_code=200)
        
        # Additional checks as needed...
    