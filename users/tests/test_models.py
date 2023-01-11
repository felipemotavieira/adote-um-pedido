from django.test import TestCase
from users.models import User


class UserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_data = {
            "first_name": "Felipe",
            "last_name": "Vieira",
            "username": "felipe_vieira",
            "email": "felipe@mail.com",
            "password": "1234",
            "cpf": "00000000000",
            "is_superuser": True,
            "is_staff": False,
        }

        cls.user = User.objects.create_user(**cls.user_data)

    def test_email_and_cpf_max_length(self):
        max_length_email = self.user._meta.get_field("email").max_length
        max_length_cpf = self.user._meta.get_field("cpf").max_length

        self.assertEqual(max_length_email, 50)
        self.assertEqual(max_length_cpf, 11)

    def test_user_fields(self):
        self.assertEqual(self.user.first_name, self.user_data["first_name"])
        self.assertEqual(self.user.last_name, self.user_data["last_name"])
        self.assertEqual(self.user.username, self.user_data["username"])
        self.assertEqual(self.user.email, self.user_data["email"])
        self.assertIsNotNone(self.user.password)
        self.assertEqual(self.user.cpf, self.user_data["cpf"])
        self.assertTrue(self.user.is_active)
        self.assertEqual(self.user.is_superuser, self.user_data["is_superuser"])
        self.assertEqual(self.user.is_staff, self.user_data["is_staff"])
        self.assertIsNone(self.user.address)
