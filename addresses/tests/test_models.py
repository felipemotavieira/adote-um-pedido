from django.test import TestCase
from addresses.models import Address


class AddressModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.address_data = {
            "state": "State",
            "city": "City",
            "street": "Street",
            "number": "000",
            "district": "District",
            "zip_code": "00000000",
        }

        cls.address = Address.objects.create(**cls.address_data)

    def test_max_lengths(self):
        state_max_length = self.address._meta.get_field("state").max_length
        city_max_length = self.address._meta.get_field("city").max_length
        street_max_length = self.address._meta.get_field("street").max_length
        district_max_length = self.address._meta.get_field("district").max_length

        self.assertEqual(state_max_length, 50)
        self.assertEqual(city_max_length, 50)
        self.assertEqual(street_max_length, 50)
        self.assertEqual(district_max_length, 50)

    def test_address_fields(self):
        self.assertEqual(self.address.state, self.address_data["state"])
        self.assertEqual(self.address.city, self.address_data["city"])
        self.assertEqual(self.address.street, self.address_data["street"])
        self.assertEqual(self.address.number, self.address_data["number"])
        self.assertEqual(self.address.district, self.address_data["district"])
        self.assertEqual(self.address.zip_code, self.address_data["zip_code"])
