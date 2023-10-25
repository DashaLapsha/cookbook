from django.test import TestCase
from django.contrib.auth import get_user

class AuthTestCase(TestCase):
    def test_login(self):
        self.assertFalse(get_user(self.client).is_authenticated())
        self.client.login(username='fred', password='secret')
        self.assertTrue(get_user(self.client).is_authenticated())