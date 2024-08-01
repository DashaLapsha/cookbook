from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .factories import UserFactory
from django.contrib.auth import get_user_model
from django.core import mail
import re
from allauth.account.models import EmailAddress
from django.core.files.uploadedfile import SimpleUploadedFile
import base64


class UserRegistrationTestCase(APITestCase):
    def test_user_can_register(self):
        image = SimpleUploadedFile("test_image.jpg", b"file_content", content_type="image/jpeg")
        data = {"username": "testuser", "email": "test@example.com", "password1": "testing*", "password2": "testing*", "profile_img": image}
        response = self.client.post(reverse('register'), data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(mail.outbox), 1)

        email_body = mail.outbox[0].body
        match = re.search(r'/users/account-confirm-email/([^/]+)/', email_body)
        confirmation_key = match.group(1)
        self.assertIsNotNone(confirmation_key)

        response = self.client.post(reverse('account_confirm_email', args=[confirmation_key]))
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

        user = get_user_model().objects.get(username="testuser")
        email_address = user.emailaddress_set.get(email="test@example.com")
        self.assertTrue(email_address.verified)


class UserLoginTestCase(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.user_data = {
            "username": self.user.username,
            "email": self.user.email,
            "password": "password",
        }
        EmailAddress.objects.create(user=self.user, email=self.user.email, verified=True, primary=True)

    def test_can_login_after_email_verification(self):
        response = self.client.post(reverse('login'), self.user_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class UserLogoutTestCase(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.client.login(username=self.user.username, password="password")

    def test_user_can_logout(self):
        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class UserDetailsTestCase(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.client.force_authenticate(user=self.user)

        base64_string = (
            "iVBORw0KGgoAAAANSUhEUgAAAAUA"
            "AAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w38GIAXDIBKE0DHxgljNBAAO"
            "9TXL0Y4OHwAAAABJRU5ErkJggg=="
        )   
        self.image_content = base64.b64decode(base64_string)

        self.profile_image = SimpleUploadedFile(
            name='profile_image.jpeg',
            content=self.image_content,
            content_type='image/jpeg'
        )

    def test_can_retrieve_user_details(self):
        url = reverse('user-details', kwargs={'id': self.user.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.user.username)

    def test_can_update_user_details(self):
        url = reverse('user-details', kwargs={'id': self.user.id})
        data = {"profile_img": self.profile_image,
                "cooking_skill_lvl": "Advanced"}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['cooking_skill_lvl'], "Advanced")
