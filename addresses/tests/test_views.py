from rest_framework.test import APITestCase
from addresses.serializers import AddressSerializer
from institutions.models import Institution
from addresses.models import Address
from users.models import User


class AddressViewsTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.admin = User.objects.create_user(
            first_name="Lucas",
            last_name="Silva",
            username="lucas_silva",
            email="lucas@mail.com",
            password="1234",
            cpf="00000000000",
            is_superuser=True,
            is_staff=True,
        )

        cls.staff = User.objects.create_user(
            first_name="Leticia",
            last_name="Angelim",
            username="leticia_angelim",
            email="leticia@mail.com",
            password="1234",
            cpf="11111111111",
            is_superuser=False,
            is_staff=True,
        )

        cls.user = User.objects.create_user(
            first_name="Naiane",
            last_name="Reis",
            username="naiane_reis",
            email="naiane@mail.com",
            password="1234",
            cpf="22222222222",
            is_superuser=False,
            is_staff=False,
        )

        cls.institution_data = {
            "name": "Institution Angelim",
            "email": "angelim@mail.com",
            "cnpj": "00000000000000",
            "phone": 00000000000,
            "type": "Orfanato",
        }

        cls.address_data = {
            "state": "State",
            "city": "City",
            "street": "Street",
            "number": 000,
            "district": "District",
            "zip_code": 00000000,
        }

        cls.addresses = [Address.objects.create(**cls.address_data) for _ in range(5)]

    def authenticate_admin(self):
        response = self.client.post("/api/login/", {"username": "lucas_silva", "password": "1234"})

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")

    def authenticate_staff(self):
        response = self.client.post("/api/login/", {"username": "leticia_angelim", "password": "1234"})

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")

    def authenticate_user(self):
        response = self.client.post("/api/login/", {"username": "naiane_reis", "password": "1234"})

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")

    def test_cannot_list_addresses_without_authentication(self):
        response = self.client.get("/api/address/")

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data, {"detail": "Authentication credentials were not provided."})

    def test_admin_can_list_all_addresses(self):
        self.authenticate_admin()
        response = self.client.get("/api/address/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(self.addresses), len(response.data))

        for address in self.addresses:
            self.assertIn(AddressSerializer(instance=address).data, response.data)

    def test_cannot_create_an_address_without_authentication(self):
        response = self.client.post(
            "/api/address/",
            {
                "state": "State",
                "city": "City",
                "street": "Street",
                "number": 000,
                "district": "District",
                "zip_code": 00000000,
            },
        )

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data, {"detail": "Authentication credentials were not provided."})

    def test_admin_can_create_an_address(self):
        self.authenticate_admin()
        response = self.client.post(
            "/api/address/",
            {
                "state": "State",
                "city": "City",
                "street": "Street",
                "number": 000,
                "district": "District",
                "zip_code": 00000000,
            },
        )
        self.assertEqual(response.status_code, 201)

    def test_staff_cannot_create_an_address_without_an_institution(self):
        self.authenticate_staff()
        response = self.client.post(
            "/api/address/",
            {
                "state": "State",
                "city": "City",
                "street": "Street",
                "number": 000,
                "district": "District",
                "zip_code": 00000000,
            },
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.data,
            {"detail": "You don't have an institution yet. Create your institution first and then create the address."},
        )

    def test_staff_can_create_an_address_having_an_institution(self):
        self.authenticate_staff()
        Institution.objects.create(**self.institution_data, owner=self.staff)

        response = self.client.post(
            "/api/address/",
            {
                "state": "State",
                "city": "City",
                "street": "Street",
                "number": 000,
                "district": "District",
                "zip_code": 00000000,
            },
        )
        self.assertEqual(response.status_code, 201)

    def test_normal_user_can_create_an_address(self):
        self.authenticate_user()
        response = self.client.post(
            "/api/address/",
            {
                "state": "State",
                "city": "City",
                "street": "Street",
                "number": 000,
                "district": "District",
                "zip_code": 00000000,
            },
        )
        self.assertEqual(response.status_code, 201)

    def test_cannot_retrieve_or_update_address_without_authentication(self):
        address = self.addresses[0]
        retrieve_response = self.client.get(f"/api/address/{address.id}/")
        update_response = self.client.patch(f"/api/address/{address.id}/")

        self.assertEqual(retrieve_response.status_code, 401)
        self.assertEqual(update_response.status_code, 401)

        self.assertEqual(retrieve_response.data, {"detail": "Authentication credentials were not provided."})
        self.assertEqual(update_response.data, {"detail": "Authentication credentials were not provided."})

    def test_admin_can_retrieve_your_own_address(self):
        self.authenticate_admin()
        address = Address.objects.create(**self.address_data)
        response = self.client.get(f"/api/address/{address.id}/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["id"], str(address.id))
        self.assertEqual(AddressSerializer(instance=address).data, response.data)

    def test_admin_can_retrieve_another_user_address(self):
        self.authenticate_user()
        address = Address.objects.create(**self.address_data)

        self.authenticate_admin()
        response = self.client.get(f"/api/address/{address.id}/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["id"], str(address.id))
        self.assertEqual(AddressSerializer(instance=address).data, response.data)

    def test_staff_can_retrieve_your_own_address(self):
        self.authenticate_staff()
        Institution.objects.create(**self.institution_data, owner=self.staff)
        address = Address.objects.create(**self.address_data)
        response = self.client.get(f"/api/address/{address.id}/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["id"], str(address.id))
        self.assertEqual(AddressSerializer(instance=address).data, response.data)

    def test_staff_cannot_retrieve_another_user_address(self):
        self.authenticate_user()
        address = Address.objects.create(**self.address_data)

        self.authenticate_staff()
        response = self.client.get(f"/api/address/{address.id}/")

        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data, {"detail": "You do not have permission to perform this action."})

    def test_user_can_retrieve_your_own_address(self):
        self.authenticate_user()
        address = Address.objects.create(**self.address_data)
        response = self.client.get(f"/api/address/{address.id}/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["id"], str(address.id))
        self.assertEqual(AddressSerializer(instance=address).data, response.data)

    def test_user_cannot_retrieve_another_user_address(self):
        self.authenticate_admin()
        address = Address.objects.create(**self.address_data)

        self.authenticate_user()
        response = self.client.get(f"/api/address/{address.id}/")

        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data, {"detail": "You do not have permission to perform this action."})

    def test_admin_can_update_your_own_address(self):
        self.authenticate_admin()
        address = Address.objects.create(**self.address_data)
        response = self.client.patch(f"/api/address/{address.id}/", {"street": "Street 3"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["id"], str(address.id))
        self.assertEqual(response.data["street"], "Street 3")

    def test_admin_can_update_another_user_address(self):
        self.authenticate_user()
        address = Address.objects.create(**self.address_data)

        self.authenticate_admin()
        response = self.client.patch(f"/api/address/{address.id}/", {"street": "Street 3"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["id"], str(address.id))
        self.assertEqual(response.data["street"], "Street 3")

    def test_staff_can_update_your_own_address(self):
        self.authenticate_staff()
        Institution.objects.create(**self.institution_data, owner=self.staff)
        address = Address.objects.create(**self.address_data)
        response = self.client.patch(f"/api/address/{address.id}/", {"street": "Street 3"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["id"], str(address.id))
        self.assertEqual(response.data["street"], "Street 3")

    def test_staff_cannot_update_another_user_address(self):
        self.authenticate_user()
        address = Address.objects.create(**self.address_data)

        self.authenticate_staff()
        response = self.client.patch(f"/api/address/{address.id}/", {"street": "Street 3"})

        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data, {"detail": "You do not have permission to perform this action."})

    def test_user_can_update_your_own_address(self):
        self.authenticate_user()
        address = Address.objects.create(**self.address_data)
        response = self.client.patch(f"/api/address/{address.id}/", {"street": "Street 3"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["id"], str(address.id))
        self.assertEqual(response.data["street"], "Street 3")

    def test_user_cannot_update_another_user_address(self):
        self.authenticate_admin()
        address = Address.objects.create(**self.address_data)

        self.authenticate_user()
        response = self.client.patch(f"/api/address/{address.id}/", {"street": "Street 3"})

        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data, {"detail": "You do not have permission to perform this action."})
