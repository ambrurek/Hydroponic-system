from rest_framework import serializers
from .models import HydroponicSystem, Measurement


class HydroponicSystemSerializer(serializers.ModelSerializer):
    """
    Serializer for the HydroponicSystem model.

    Serializes HydroponicSystem instances to JSON and validates incoming data.

    Attributes:
        id (int): The unique identifier for the HydroponicSystem.
        owner (str): The username of the system owner.
        name (str): The name of the HydroponicSystem.
        description (str): A textual description of the HydroponicSystem.
    """

    owner = serializers.ReadOnlyField(source="owner.username")

    class Meta:
        model = HydroponicSystem
        fields = ["id", "owner", "name", "description"]


class MeasurementSerializer(serializers.ModelSerializer):
    """
    Serializer for the Measurement model.

    Serializes Measurement instances to JSON and validates incoming data.

    Attributes:
        id (int): The unique identifier for the Measurement.
        system (int): The ID of the HydroponicSystem to which the measurement belongs.
        data (datetime): The timestamp indicating when the measurement was recorded.
        ph (float): The pH value of the measurement.
        temperature_raw (str): The raw temperature data with units (e.g., "25C").
        tds (float): The Total Dissolved Solids (TDS) value of the measurement.
    """

    class Meta:
        model = Measurement
        fields = ["id", "system", "data", "ph", "temperature_raw", "tds"]
