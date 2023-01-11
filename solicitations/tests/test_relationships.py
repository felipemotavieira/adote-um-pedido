from django.test import TestCase
from django.db import IntegrityError
from donees.models import Donee
from solicitations.models import Solicitation
from users.models import User
from addresses.models import Address
from institutions.models import Institution
import ipdb
class SolicitationsModelTest(TestCase):
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

        cls.solicitation_data = {
            "description": "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book",

        }

        cls.donee_data = {
            "name": "Pedro Rocha",
            "age": "09",  
        }


    def test_if_solicitation_can_have_a_donne(self):
        created_owner = User.objects.create_user(**self.user_data)
        institution = Institution.objects.create(**self.institution_data, owner=created_owner)
        donee = Donee.objects.create(**self.donee_data, institution= institution)
        solicitation = Solicitation.objects.create(**self.solicitation_data, donee= donee , institution=institution)
        self.assertIs(solicitation.donee, donee)

    def test_if_raise_error_when_solicitation_do_not_have_a_donee(self):
        with self.assertRaises(IntegrityError):
            Solicitation.objects.create(**self.solicitation_data)

   
