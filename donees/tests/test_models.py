from django.test import TestCase
from users.models import User
from institutions.models import Institution
from donees.models import Donee


class DoneeModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):

        cls.staff_data = {
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

        cls.donee_data = {
            "name": "Pedro Rocha",
            "age": "09",  
        }
        
        cls.staff = User.objects.create_user(**cls.staff_data)
        cls.institution = Institution.objects.create(**cls.institution_data, owner=cls.staff)
        cls.donee = Donee.objects.create(**cls.donee_data, institution=cls.institution)

    def test_max_lengths(self):
        name_max_length = self.donee._meta.get_field("name").max_length
        self.assertEqual(name_max_length, 50)
        
    def test_institution_fields(self):
        self.assertEqual(self.donee.name, self.donee_data["name"])
        self.assertEqual(self.donee.age, self.donee_data["age"])

  