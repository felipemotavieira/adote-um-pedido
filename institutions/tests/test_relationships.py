from django.test import TestCase
from django.db import IntegrityError

from users.models import User
from addresses.models import Address
from institutions.models import Institution


class InstitutionModelTest(TestCase):
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
            "is_staff": True,
        }

        cls.address_data = {
            "state": "State",
            "city": "City",
            "street": "Street",
            "number": 000,
            "district": "District",
            "zip_code": 00000000,
        }

        cls.institution_data = {
            "name": "Institution Oliveira",
            "email": "oliveira@mail.com",
            "cnpj": "00000000000000",
            "phone": 00000000000,
            "type": "Orfanato",
        }

    def test_if_institution_can_have_a_owner(self):
        created_owner = User.objects.create_user(**self.user_data)
        institution = Institution.objects.create(**self.institution_data, owner=created_owner)

        self.assertIs(institution.owner, created_owner)

    def test_if_raise_error_when_institution_do_not_have_a_owner(self):
        with self.assertRaises(IntegrityError):
            Institution.objects.create(**self.institution_data)

    def test_if_institution_can_have_a_address(self):
        owner = User.objects.create_user(**self.user_data)
        created_address = Address.objects.create(**self.address_data)
        institution = Institution.objects.create(**self.institution_data, owner=owner, address=created_address)

        self.assertIs(institution.address, created_address)
