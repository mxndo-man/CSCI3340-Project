from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class SignUpViewTests(TestCase):
    def test_signup_logs_user_in_and_redirects_home(self):
        response = self.client.post(
            reverse("accounts:signup"),
            {
                "email": "new-user@example.com",
                "username": "new-user",
                "password1": "Strong-password-834!",
                "password2": "Strong-password-834!",
            },
        )

        self.assertRedirects(response, reverse("home"), fetch_redirect_response=False)
        user = get_user_model().objects.get(username="new-user")
        self.assertEqual(int(self.client.session["_auth_user_id"]), user.pk)
