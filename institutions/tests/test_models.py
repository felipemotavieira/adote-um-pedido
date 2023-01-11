from django.test import TestCase
from users.models import User
from institutions.models import Institution


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

        cls.repr = User.objects.create_user(**cls.repr_data)
        cls.institution = Institution.objects.create(**cls.institution_data, owner=cls.repr)

    def test_max_lengths(self):
        name_max_length = self.institution._meta.get_field("name").max_length
        email_max_length = self.institution._meta.get_field("email").max_length
        cnpj_max_length = self.institution._meta.get_field("cnpj").max_length

        self.assertEqual(name_max_length, 50)
        self.assertEqual(email_max_length, 50)
        self.assertEqual(cnpj_max_length, 14)

    def test_institution_fields(self):
        self.assertEqual(self.institution.name, self.institution_data["name"])
        self.assertEqual(self.institution.email, self.institution_data["email"])
        self.assertEqual(self.institution.cnpj, self.institution_data["cnpj"])
        self.assertEqual(self.institution.phone, self.institution_data["phone"])
        self.assertEqual(self.institution.type, self.institution_data["type"])
        self.assertTrue(self.institution.is_active)
        self.assertEqual(self.institution.status, "Under examination")
