from django.test import TestCase
from django.db import IntegrityError

from users.models import User
from institutions.models import Institution
from donees.models import Donee


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

        cls.donee_data = {
            "name": "Pedro Rocha",
            "age": "09",  
        }

    def test_if_donee_can_have_a_institution(self):
        created_owner = User.objects.create_user(**self.user_data)
        institution = Institution.objects.create(**self.institution_data, owner=created_owner)
        donee = Donee.objects.create(**self.donee_data, institution=institution)

        self.assertIs(donee.institution, institution)

    def test_if_raise_error_when_donee_do_not_have_a_institution(self):
        with self.assertRaises(IntegrityError):
            Donee.objects.create(**self.donee_data)

   
