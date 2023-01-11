from django.test import TestCase
from users.models import User
from institutions.models import Institution
from donees.models import Donee
from solicitations.models import Solicitation

class InstitutionModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.repr_data = {
            "first_name": "Lucas",
            "last_name": "Galvão",
            "username": "lucas_galvao",
            "email": "lucas@mail.com",
            "password": "1234",
            "cpf": "00000000000",
            "is_superuser": False,
            "is_staff": True,
        }

        cls.institution_data = {
            "name": "Institution Galvão",
            "email": "galvao@mail.com",
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

        cls.repr = User.objects.create_user(**cls.repr_data)
        cls.institution = Institution.objects.create(**cls.institution_data, owner=cls.repr)
        cls.donee = Donee.objects.create(**cls.donee_data, institution=cls.institution)
        cls.solicitation = Solicitation.objects.create(**cls.solicitation_data, donee=cls.donee , institution=cls.institution)

    def test_max_lengths(self):
        description_max_length = self.solicitation._meta.get_field("description").max_length
        self.assertEqual(description_max_length, 200)
        
    def test_solicitation_fields(self):
        self.assertEqual(self.solicitation.description, self.solicitation_data["description"])
       
