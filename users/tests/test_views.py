from rest_framework.test import APITestCase
from users.models import User
from users.serializers import UserSerializer


class UserViewsTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.admin_data = {
            "first_name": "Lucas",
            "last_name": "Silva",
            "username": "lucas_silva",
            "email": "lucas@mail.com",
            "password": "1234",
            "cpf": "00000000000",
            "is_superuser": True,
            "is_staff": True,
        }

        cls.user_data = {
            "first_name": "Naiane",
            "last_name": "Reis",
            "username": "naiane_reis",
            "email": "naiane@mail.com",
            "password": "1234",
            "cpf": "11111111111",
            "is_superuser": False,
            "is_staff": False,
        }

        cls.admin = User.objects.create_user(**cls.admin_data)
        cls.user = User.objects.create_user(**cls.user_data)
        cls.users = [cls.admin, cls.user]

    def authenticate_admin(self):
        response = self.client.post("/api/login/", {"username": "lucas_silva", "password": "1234"})

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")

    def authenticate_user(self):
        response = self.client.post("/api/login/", {"username": "naiane_reis", "password": "1234"})

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")

    def test_cannot_list_users_without_authentication(self):
        response = self.client.get("/api/users/")

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data, {"detail": "Authentication credentials were not provided."})

    def test_not_admin_cannot_list_users(self):
        self.authenticate_user()
        response = self.client.get("/api/users/")

        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data, {"detail": "You do not have permission to perform this action."})

    def test_admin_can_list_all_users(self):
        self.authenticate_admin()
        response = self.client.get("/api/users/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(self.users), len(response.data))

        for user in self.users:
            self.assertIn(UserSerializer(instance=user).data, response.data)

    def test_cannot_retrieve_or_update_or_delete_user_without_authentication(self):
        user = self.users[0]
        retrieve_response = self.client.get(f"/api/users/{user.id}/")
        update_response = self.client.patch(f"/api/users/{user.id}/")
        delete_response = self.client.delete(f"/api/users/{user.id}/")

        self.assertEqual(retrieve_response.status_code, 401)
        self.assertEqual(update_response.status_code, 401)
        self.assertEqual(delete_response.status_code, 401)

        self.assertEqual(retrieve_response.data, {"detail": "Authentication credentials were not provided."})
        self.assertEqual(update_response.data, {"detail": "Authentication credentials were not provided."})
        self.assertEqual(delete_response.data, {"detail": "Authentication credentials were not provided."})

    def test_not_admin_cannot_retrieve_another_user(self):
        self.authenticate_user()
        user = self.users[0]
        response = self.client.get(f"/api/users/{user.id}/")

        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data, {"detail": "You do not have permission to perform this action."})

    def test_not_admin_cannot_update_another_user(self):
        self.authenticate_user()
        user = self.users[0]
        response = self.client.patch(f"/api/users/{user.id}/")

        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data, {"detail": "You do not have permission to perform this action."})

    def test_not_admin_cannot_delete_another_user(self):
        self.authenticate_user()
        user = self.users[0]
        response = self.client.delete(f"/api/users/{user.id}/")

        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.data, {"detail": "You do not have permission to perform this action."})

    def test_not_admin_can_retrieve_your_own_profile(self):
        self.authenticate_user()
        user = self.users[1]
        response = self.client.get(f"/api/users/{user.id}/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["id"], str(user.id))
        self.assertEqual(UserSerializer(instance=user).data, response.data)

    def test_not_admin_can_update_your_own_profile(self):
        self.authenticate_user()
        user = self.users[1]
        response = self.client.patch(f"/api/users/{user.id}/", {"email": "naiane@hotmail.com"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["id"], str(user.id))
        self.assertEqual(response.data["email"], "naiane@hotmail.com")

    def test_not_admin_can_delete_your_own_profile(self):
        self.authenticate_user()
        user = self.users[1]
        response = self.client.delete(f"/api/users/{user.id}/")

        self.authenticate_admin()
        deleted = self.client.get(f"/api/users/{user.id}/")

        self.assertEqual(response.status_code, 204)
        self.assertIsNone(response.data)
        self.assertFalse(deleted.data["is_active"])

    def test_admin_can_retrieve_another_user(self):
        self.authenticate_admin()
        user = self.users[1]
        response = self.client.get(f"/api/users/{user.id}/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["id"], str(user.id))
        self.assertEqual(UserSerializer(instance=user).data, response.data)

    def test_admin_can_update_another_user(self):
        self.authenticate_admin()
        user = self.users[1]
        response = self.client.patch(f"/api/users/{user.id}/", {"email": "naiane@hotmail.com"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["id"], str(user.id))
        self.assertEqual(response.data["email"], "naiane@hotmail.com")

    def test_admin_can_delete_another_user(self):
        self.authenticate_admin()
        user = self.users[1]
        response = self.client.delete(f"/api/users/{user.id}/")
        deleted = self.client.get(f"/api/users/{user.id}/")

        self.assertEqual(response.status_code, 204)
        self.assertIsNone(response.data)
        self.assertFalse(deleted.data["is_active"])

    def test_admin_can_retrieve_your_own_profile(self):
        self.authenticate_admin()
        user = self.users[0]
        response = self.client.get(f"/api/users/{user.id}/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["id"], str(user.id))
        self.assertEqual(UserSerializer(instance=user).data, response.data)

    def test_admin_can_update_your_own_profile(self):
        self.authenticate_admin()
        user = self.users[0]
        response = self.client.patch(f"/api/users/{user.id}/", {"email": "lucas@hotmail.com"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["id"], str(user.id))
        self.assertEqual(response.data["email"], "lucas@hotmail.com")

    def test_admin_can_delete_your_own_profile(self):
        self.authenticate_admin()
        user = self.users[0]
        response = self.client.delete(f"/api/users/{user.id}/")

        self.assertEqual(response.status_code, 204)
        self.assertIsNone(response.data)
