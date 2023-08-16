from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.auth import get_user

class RegistrationTestCase(TestCase):
    def test_user_account_is_created(self):
        self.client.post(
            reverse("users:register"),
            data={
                "username":"yannmartel",
                "first_name":"Yann",
                "last_name":"Martel",
                "email":"yannmartel@gmail.com",
                "password":"somepass"
            }
        )

        user = User.objects.get(username="yannmartel")
        self.assertEqual(user.first_name, "Yann")
        self.assertEqual(user.last_name, "Martel")
        self.assertEqual(user.email, "yannmartel@gmail.com")
        self.assertNotEqual(user.password, "somepass")
        self.assertTrue(user.check_password("somepass"))

    def test_required_fields(self):
        response = self.client.post(
            reverse("users:register"),
            data = {
                "first_name":"Samandar",
                "email":"sam4@gmail.com",
            }
        )

        # Bu test db dagi userlar sonini sanaydi, tabiiyki u 0.
        user_count = User.objects.count()

        self.assertEqual(user_count, 0)
        # Response ichida kelayotgan formani tekshiramiz. Bunda "form" - views.py da post metod uchun context sifatida chiqarilgan variable. formdagi usernamening errori shunday bolishiga test qilyapmiz
        self.assertFormError(response, "form", "username", "This field is required.")
        self.assertFormError(response, "form", "password", "This field is required.")

    def test_invalid_email(self):
        response = self.client.post(
            reverse("users:register"),
            data={
                "username":"yannmartel",
                "first_name":"Yann",
                "last_name":"Martel",
                "email":"invalid-email",
                "password":"somepass"
            }
        )

        user_count = User.objects.count()
        self.assertEqual(user_count, 0)
        self.assertFormError(response, "form", "email", "Enter a valid email address.")

    # Task - User already exists
    def test_duplicate_user(self):
        # self.client.post(
        #     reverse("users:register"),
        #     data = {
        #         "username":"yannmartel",
        #         "first_name":"Yann",
        #         "last_name":"Martel",
        #         "email":"yannmartel@gmail.com",
        #         "password":"thththtrh"
        #     }
        # )
        user = User.objects.create(username='yannmartel', first_name="Yann")
        user.set_password("somepass")
        user.save()
        
        response2 = self.client.post(
            reverse("users:register"),
            data = {
                "username":"yannmartel",
                "first_name":"Yann",
                "last_name":"Martel",
                "email":"yannmartel@gmail.com",
                "password":"thththtrh"
            }
        )
        user_count = User.objects.count()
        self.assertEqual(user_count, 1)

        self.assertFormError(response2, "form", "username", "A user with that username already exists.")


class LoginTestCase(TestCase):
    def test_successful_login(self):
        db_user = User.objects.create(username="samandar", first_name="Samandar")
        db_user.set_password("sam0704@")
        db_user.save()

        self.client.post(
            reverse("users:login"),
            data = {
                "username":"samandar",
                "password":"sam0704@"
            }
        )

        user = get_user(self.client)
        self.assertTrue(user.is_authenticated)

    def test_wrong_credentials(self):
        db_user = User.objects.create(username="samandar", first_name="Samandar")
        db_user.set_password("sam0704@")
        db_user.save()

        self.client.post(
            reverse("users:login"),
            data = {
                "username":"samanda",
                "password":"sam0704@"
            }
        )

        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)

        # password check
        self.client.post(
            reverse("users:login"),
            data = {
                "username":"samandar",
                "password":"sam0704!"
            }
        )

        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)