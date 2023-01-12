from rest_framework.test import APITestCase
from institutions.serializers import InstitutionSerializer
from institutions.models import Institution
from users.models import User


class InstitutionsViewsTest(APITestCase):
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

        cls.staff = User.objects.create_user(
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
            "name": "Institution Oliveira",
            "email": "oliveira@mail.com",
            "cnpj": "00000000000000",
            "phone": 00000000000,
            "type": "Orfanato",
        }

        cls.institution2_data = {
            "name": "Institution Oliveira",
            "email": "institution@mail.com",
            "cnpj": "11111111111111",
            "phone": 00000000000,
            "type": "Orfanato",
        }

        cls.institution_test = {
            "name": "Institution Test",
            "email": "test@mail.com",
            "cnpj": "2222222222222",
            "phone": 00000000000,
            "type": "Orfanato",
        }

        cls.institution1 = Institution.objects.create(**cls.institution1_data, owner=cls.staff2)
        cls.institution2 = Institution.objects.create(**cls.institution2_data, owner=cls.staff3)
        cls.institutions = [cls.institution1, cls.institution2]

    def authenticate_admin(self):
        response = self.client.post("/api/login/", {"username": "naiane_reis", "password": "1234"})

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")

    def authenticate_staff(self):
        response = self.client.post("/api/login/", {"username": "livia_oliveira", "password": "1234"})

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")

    def authenticate_user(self):
        response = self.client.post("/api/login/", {"username": "felipe_vieira", "password": "1234"})

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")

    def test_can_list_all_institutions(self):
        response = self.client.get("/api/institutions/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(self.institutions), len(response.data))

        for institution in self.institutions:
            self.assertIn(InstitutionSerializer(instance=institution).data, response.data)

    def test_cannot_create_an_institution_without_authentication(self):
        response = self.client.post(
            "/api/institutions/",
            {
                "name": "Institution Oliveira",
                "email": "institution@mail.com",
                "cnpj": "11111111111111",
                "phone": 00000000000,
                "type": "Orfanato",
            },
        )

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data, {"detail": "Authentication credentials were not provided."})

    def test_normal_user_cannot_create_an_institution(self):
        self.authenticate_user()
        response = self.client.post(
            "/api/institutions/",
            {
                "name": "Institution Oliveira",
                "email": "institution@mail.com",
                "cnpj": "11111111111111",
                "phone": 00000000000,
                "type": "Orfanato",
            },
        )

        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data, {"detail": "You do not have permission to perform this action."})

    def test_staff_can_create_an_institution(self):
        self.authenticate_staff()
        response = self.client.post(
            "/api/institutions/",
            {
                "name": "Institution Oliveira",
                "email": "teste@mail.com",
                "cnpj": "2222222222222",
                "phone": 00000000000,
                "type": "Orfanato",
            },
        )
        self.assertEqual(response.status_code, 201)

    def test_admin_can_create_an_institution(self):
        self.authenticate_admin()
        response = self.client.post(
            "/api/institutions/",
            {
                "name": "Institution Oliveira",
                "email": "teste@mail.com",
                "cnpj": "2222222222222",
                "phone": 00000000000,
                "type": "Orfanato",
            },
        )
        self.assertEqual(response.status_code, 201)

    def test_can_retrieve_an_institution(self):
        institution = self.institutions[0]
        response = self.client.get(f"/api/institutions/{institution.id}/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["id"], str(institution.id))
        self.assertEqual(InstitutionSerializer(instance=institution).data, response.data)

    def test_cannot_update_or_delete_institution_without_authentication(self):
        institution = self.institutions[0]
        update_response = self.client.patch(f"/api/institutions/{institution.id}/")
        delete_response = self.client.delete(f"/api/institutions/{institution.id}/")

        self.assertEqual(update_response.status_code, 401)
        self.assertEqual(delete_response.status_code, 401)

        self.assertEqual(update_response.data, {"detail": "Authentication credentials were not provided."})
        self.assertEqual(delete_response.data, {"detail": "Authentication credentials were not provided."})

    def test_normal_user_cannot_update_an_institution(self):
        self.authenticate_user()
        institution = self.institutions[0]
        response = self.client.patch(f"/api/institutions/{institution.id}/")

        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data, {"detail": "You do not have permission to perform this action."})

    def test_normal_user_cannot_delete_an_institution(self):
        self.authenticate_user()
        institution = self.institutions[0]

        response = self.client.delete(f"/api/institutions/{institution.id}/")

        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data, {"detail": "You do not have permission to perform this action."})

    def test_admin_can_update_an_institution(self):
        self.authenticate_admin()
        institution = self.institutions[0]
        response = self.client.patch(f"/api/institutions/{institution.id}/", {"name": "Institution"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["id"], str(institution.id))
        self.assertEqual(response.data["name"], "Institution")

    def test_admin_can_delete_an_institution(self):
        self.authenticate_admin()
        institution = self.institutions[0]
        response = self.client.delete(f"/api/institutions/{institution.id}/")
        deleted = self.client.get(f"/api/institutions/{institution.id}/")

        self.assertEqual(response.status_code, 204)
        self.assertIsNone(response.data)
        self.assertFalse(deleted.data["is_active"])

    def test_staff_can_update_your_own_institution(self):
        self.authenticate_staff()
        institution = Institution.objects.create(**self.institution_test, owner=self.staff)
        response = self.client.patch(f"/api/institutions/{institution.id}/", {"name": "Institution"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["id"], str(institution.id))
        self.assertEqual(response.data["name"], "Institution")

    def test_staff_can_delete_your_own_institution(self):
        self.authenticate_staff()
        institution = Institution.objects.create(**self.institution_test, owner=self.staff)
        response = self.client.delete(f"/api/institutions/{institution.id}/")
        deleted = self.client.get(f"/api/institutions/{institution.id}/")

        self.assertEqual(response.status_code, 204)
        self.assertIsNone(response.data)
        self.assertFalse(deleted.data["is_active"])

    def test_staff_cannot_update_another_staff_institution(self):
        self.authenticate_staff()
        institution = self.institutions[0]
        response = self.client.patch(f"/api/institutions/{institution.id}/", {"name": "Institution"})

        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data, {"detail": "You do not have permission to perform this action."})

    def test_staff_cannot_delete_another_staff_institution(self):
        self.authenticate_staff()
        institution = self.institutions[0]
        response = self.client.delete(f"/api/institutions/{institution.id}/")

        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data, {"detail": "You do not have permission to perform this action."})
