from rest_framework.test import APITestCase
from donees.serializers import DoneeSerializers
from donees.models import Donee
from institutions.serializers import InstitutionSerializer
from institutions.models import Institution
from users.models import User
import ipdb

class DoneeseViewsTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.admin = User.objects.create_user(
            first_name="Naiane",
            last_name="Reis",
            username="naiane_reis",
            email="naiane@mail.com",
            password="1234",
            cpf="00000000000",
            is_superuser=True,
            is_staff=True,
        )

        cls.staff1 = User.objects.create_user(
            first_name="Livia",
            last_name="Oliveira",
            username="livia_oliveira",
            email="livia@mail.com",
            password="1234",
            cpf="11111111111",
            is_superuser=False,
            is_staff=True,
        )

        cls.staff2 = User.objects.create_user(
            first_name="Lucas",
            last_name="Galvão",
            username="lucas_galvao",
            email="lucas@mail.com",
            password="1234",
            cpf="22222222222",
            is_superuser=False,
            is_staff=True,
        )

        cls.staff3 = User.objects.create_user(
            first_name="Lucas",
            last_name="Silva",
            username="lucas_silva",
            email="lucass@mail.com",
            password="1234",
            cpf="33333333333",
            is_superuser=False,
            is_staff=True,
        )

        cls.user = User.objects.create_user(
            first_name="Felipe",
            last_name="Vieira",
            username="felipe_vieira",
            email="felipe@mail.com",
            password="1234",
            cpf="44444444444",
            is_superuser=False,
            is_staff=False,
        )

        cls.institution1_data = {
            "name": "Institution 1",
            "email": "institution1@mail.com",
            "cnpj": "1111111111111111",
            "phone": 00000000000,
            "type": "Orfanato",
        }

        cls.institution2_data = {
            "name": "Institution 2",
            "email": "institution2@mail.com",
            "cnpj": "222222222222222",
            "phone": 00000000000,
            "type": "Orfanato",
        }

        cls.institution3_data = {
            "name": "Institution 3",
            "email": "institution3@mail.com",
            "cnpj": "333333333333333",
            "phone": 00000000000,
            "type": "Orfanato",
        }

        cls.donee1_data = {
            "name": "Pedro Rocha",
            "age": "09",  
        }

        cls.donee2_data = {
            "name": "Maria Victória",
            "age": "02",  
        }

        cls.donee3_data = {
            "name": "Gustavo Silva",
            "age": "05",  
        }
        
        cls.institution1 = Institution.objects.create(**cls.institution1_data, owner=cls.staff3)
        cls.institution2 = Institution.objects.create(**cls.institution2_data, owner=cls.staff2)
        cls.institution3 = Institution.objects.create(**cls.institution3_data, owner=cls.staff1)
        cls.donee1 = Donee.objects.create(**cls.donee1_data, institution=cls.institution1)
        cls.donee2 = Donee.objects.create(**cls.donee2_data, institution=cls.institution2)
        cls.donee3 = Donee.objects.create(**cls.donee3_data, institution=cls.institution1)
        cls.donee4 = Donee.objects.create(**cls.donee3_data, institution=cls.institution3)
        cls.donees = [cls.donee1, cls.donee2, cls.donee3, cls.donee4]

    def authenticate_admin(self):

        response = self.client.post("/api/login/", {"username": "naiane_reis", "password": "1234"})
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")

    def authenticate_staff(self):

        response = self.client.post("/api/login/", {"username": "livia_oliveira", "password": "1234"})
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")
    
    def authenticate_staff2(self):

        response = self.client.post("/api/login/", {"username": "lucas_galvao", "password": "1234"})
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")

    def authenticate_user(self):

        response = self.client.post("/api/login/", {"username": "felipe_vieira", "password": "1234"})
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")

    def test_can_list_all_donees(self):

        response = self.client.get("/api/donees/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(self.donees), len(response.data))
        
        for donee in self.donees:
            self.assertIn(DoneeSerializers(instance=donee).data, response.data)
     
    def test_cannot_create_donee_without_authentication(self):

        response = self.client.post("/api/donees/",
            {
                "name": "Arthur Silva",
                "age": "09",
                "institution": self.institution1.id
            }
        )

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data, {"detail": "Authentication credentials were not provided."})

    def test_adm_can_create_a_donnee(self):
        self.authenticate_admin()
        response = self.client.post("/api/donees/",
            {
                "name": "Arthur Silva",
                "age": "09",
                "institution": self.institution1.id
            }
        )
        self.assertEqual(response.status_code, 201)

    def test_normal_user_cannot_create_an_donee(self):

        self.authenticate_user()
        response = self.client.post("/api/donees/",
            {
                "name": "Arthur Silva",
                "age": "09",
                "institution": self.institution1.id
            }
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data, {"detail": "You do not have permission to perform this action."})

   
    def test_staff_owner_intitution_can_create_a_donee(self):
        self.authenticate_staff()
        response = self.client.post( "/api/donees/",
            {
                "name": "Arthur Silva",
                "age": "09",
                "institution": self.institution3.id
            }
        )
        self.assertEqual(response.status_code, 201)

    def test_staff_no_owner_intitution_cant_create_a_donee(self):
        self.authenticate_staff2()
        response = self.client.post( "/api/donees/",
            {
                "name": "Arthur Silva",
                "age": "09",
                "institution": self.institution3.id
            }
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data, {"detail": "You do not have permission to perform this action."})

    def test_user_create_a_donee(self):

        self.authenticate_user()
        response = self.client.post( "/api/donees/",
            {
                "name": "Arthur Silva",
                "age": "09",
                "institution": self.institution3.id
            }
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data, {"detail": "You do not have permission to perform this action."})

    def test_can_retrieve_a_donee(self):

        donee = self.donees[0]
        response = self.client.get(f"/api/donees/{donee.id}/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["id"], str(donee.id))
        self.assertEqual(DoneeSerializers(instance=donee).data, response.data)

    def test_cannot_update_or_delete_institution_without_authentication(self):
        donee = self.donees[0]
        update_response = self.client.patch(f"/api/donees/{donee.id}/")
        delete_response = self.client.delete(f"/api/donees/{donee.id}/")

        self.assertEqual(update_response.status_code, 401)
        self.assertEqual(delete_response.status_code, 401)

        self.assertEqual(update_response.data, {"detail": "Authentication credentials were not provided."})
        self.assertEqual(delete_response.data, {"detail": "Authentication credentials were not provided."})

    def test_normal_user_cannot_update_a_donee(self):
        self.authenticate_user()
        donee = self.donees[0]
        response = self.client.patch(f"/api/donees/{donee.id}/")
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data, {"detail": "You do not have permission to perform this action."})

    def test_normal_user_cannot_delete_a_donee(self):
        self.authenticate_user()
        donee = self.donees[0]
        response = self.client.patch(f"/api/donees/{donee.id}/")
        response = self.client.delete(f"/api/donees/{donee.id}/")
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data, {"detail": "You do not have permission to perform this action."})

    def test_admin_can_update_a_donee(self):
        self.authenticate_admin()
        donee = self.donees[0]
        response = self.client.patch(f"/api/donees/{donee.id}/", {"name": "Pedro Perreira"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["id"], str(donee.id))
        self.assertEqual(response.data["name"], "Pedro Perreira")

    def test_admin_can_delete_a_donee(self):
        self.authenticate_admin()
        donee = self.donees[0]
        response = self.client.delete(f"/api/donees/{donee.id}/")
    
        self.assertEqual(response.status_code, 204)
        self.assertIsNone(response.data)
        self.assertEqual(response.data, None)

    def test_staff_can_update_your_own_donee(self):
        self.authenticate_staff()
        donee = self.donees[3]
        
        response = self.client.patch(f"/api/donees/{donee.id}/", {"age": 3})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["id"], str(donee.id))
        self.assertEqual(response.data["age"], 3)

    def test_staff_can_delete_your_own_donee(self):

        self.authenticate_staff()
        donee = self.donees[3]
        response = self.client.delete(f"/api/donees/{donee.id}/")
        
        self.assertEqual(response.status_code, 204)
        self.assertIsNone(response.data, None)
   

    def test_staff_cannot_update_another_staff_donee(self):

        self.authenticate_staff2()
        donee = self.donees[3]
        response = self.client.patch(f"/api/donees/{donee.id}/", {"name": "Pedro Perreira"})

        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data, {"detail": "You do not have permission to perform this action."})

    def test_staff_cannot_delete_another_staff_donee(self):
        self.authenticate_staff2()
        donee = self.donees[3]
        response = self.client.delete(f"/api/donees/{donee.id}/")

        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data, {"detail": "You do not have permission to perform this action."})
