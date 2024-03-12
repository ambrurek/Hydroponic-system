from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token
from .models import HydroponicSystem, Measurement


class HydroponicSystemAPITestCase(TestCase):
    """
    Test case for HydroponicSystem API views.
    """

    def setUp(self):
        """
        Set up initial data for tests.
        """
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.system = HydroponicSystem.objects.create(
            owner=self.user, name="Test System"
        )
        self.client = APIClient()

        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")

    def test_hydroponic_system_list_create(self):
        """
        Test listing and creating HydroponicSystems.
        """
        # Ensure we can list hydroponic systems
        response = self.client.get("/systems/hydroponic-systems/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Ensure we can create a new hydroponic system
        data = {"owner": self.user.id, "name": "New System"}
        response = self.client.post("/systems/hydroponic-systems/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_hydroponic_system_detail(self):
        """
        Test retrieving details of a HydroponicSystem.
        """
        # Ensure we can retrieve details of a hydroponic system
        response = self.client.get(f"/systems/hydroponic-systems/{self.system.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_measurement_list_create(self):
        """
        Test listing and creating Measurements.
        """
        # Ensure we can list measurements
        response = self.client.get("/systems/measurements/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Ensure we can create a new measurement
        data = {
            "system": self.system.id,
            "data": "2024-03-05",
            "ph": 6.5,
            "temperature_raw": "25C",
            "tds": 500,
        }
        response = self.client.post("/systems/measurements/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_measurement_detail(self):
        """
        Test retrieving details of a Measurement.
        """
        # Ensure we can retrieve details of a measurement
        measurement = Measurement.objects.create(
            system=self.system,
            data="2024-03-05",
            ph=6.5,
            temperature_raw="25C",
            tds=500,
        )
        response = self.client.get(f"/systems/measurements/{measurement.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
