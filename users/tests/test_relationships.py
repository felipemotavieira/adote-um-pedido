from django.test import TestCase
from django.db import IntegrityError

from users.models import User
from addresses.models import Address


class UserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_data = {
            "first_name": "Lívia",
            "last_name": "Oliveira",
            "username": "livia_oliveira",
            "email": "livia@mail.com",
            "password": "1234",
            "cpf": "00000000000",
            "is_superuser": False,
            "is_staff": False,
        }

        cls.user = User.objects.create_user(**cls.user_data)

        cls.address_data = {
            "state": "State",
            "city": "City",
            "street": "Street",
            "number": "000",
            "district": "District",
            "zip_code": "00000000",
        }

    def test_if_user_can_have_a_address(self):
        created_address = Address.objects.create(**self.address_data)

        self.user.address = created_address
        self.user.save()

        self.assertIs(self.user.address, created_address)

    def test_if_raise_error_when_address_already_have_an_user(self):
        created_address = Address.objects.create(**self.address_data)

        self.user.address = created_address
        self.user.save()

        with self.assertRaises(IntegrityError):
            user_two = User.objects.create_user(
                first_name="Lucas",
                last_name="Galvão",
                username="lucas_galvao",
                email="lucas@mail.com",
                password="1234",
                cpf="11111111111",
                is_superuser=False,
                is_staff=False,
            )
            user_two.address = created_address
            user_two.save()
