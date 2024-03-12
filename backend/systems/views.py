from rest_framework import generics, serializers
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import HydroponicSystem, Measurement
from .serializers import HydroponicSystemSerializer, MeasurementSerializer


class HydroponicSystemList(generics.ListCreateAPIView):
    """
    API view for listing and creating HydroponicSystems.

    Attributes:
        queryset (QuerySet): The set of HydroponicSystem objects.
        serializer_class (HydroponicSystemSerializer): The serializer class for HydroponicSystem.
        authentication_classes (list): The authentication classes required for this view.
        permission_classes (list): The permission classes required for this view.
    """

    queryset = HydroponicSystem.objects.all()
    serializer_class = HydroponicSystemSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """
        Perform create operation and assign the owner to the current user.
        """
        serializer.save(owner=self.request.user)


class HydroponicSystemDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    API view for retrieving, updating, and deleting a HydroponicSystem.

    Attributes:
        queryset (QuerySet): The set of HydroponicSystem objects.
        serializer_class (HydroponicSystemSerializer): The serializer class for HydroponicSystem.
        authentication_classes (list): The authentication classes required for this view.
        permission_classes (list): The permission classes required for this view.
    """

    queryset = HydroponicSystem.objects.all()
    serializer_class = HydroponicSystemSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve details of a HydroponicSystem and its last X measurements.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        # Get the last X measurements for the system
        x = request.query_params.get(
            "last_measurements", 10
        )  # Default to 10 measurements
        measurements = instance.measurements.all().order_by("-data")[:x]
        measurement_serializer = MeasurementSerializer(measurements, many=True)

        # Add the list of measurements to the response data
        response_data = serializer.data
        response_data["last_measurements"] = measurement_serializer.data

        return Response(response_data)


class MeasurementListCreate(generics.ListCreateAPIView):
    """
    API view for listing and creating Measurements.

    Attributes:
        queryset (QuerySet): The set of Measurement objects.
        serializer_class (MeasurementSerializer): The serializer class for Measurement.
        authentication_classes (list): The authentication classes required for this view.
        permission_classes (list): The permission classes required for this view.
    """

    queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """
        Perform create operation and convert temperature to Celsius.
        """
        system_id = self.request.data.get("system", None)
        if system_id:
            temperature_raw = serializer.validated_data["temperature_raw"]
            temperature_celsius = self.convert_to_celsius(temperature_raw)
            serializer.save(
                system_id=system_id,
                data=self.request.data.get("data", None),
                ph=self.request.data.get("ph", None),
                temperature_raw=temperature_celsius,
                tds=self.request.data.get("tds", None),
            )

    def convert_to_celsius(self, temperature_raw):
        """
        Convert temperature from Fahrenheit to Celsius if in Fahrenheit format.
        """
        if "C" in temperature_raw:
            return int(temperature_raw.replace("C", ""))
        elif "F" in temperature_raw:
            fahrenheit = int(temperature_raw.replace("F", ""))
            return round((fahrenheit - 32) * 5 / 9, 2)
        else:
            raise serializers.ValidationError(
                "Invalid temperature format. Use 'C' or 'F'."
            )


class MeasurementDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    API view for retrieving, updating, and deleting a Measurement.

    Attributes:
        queryset (QuerySet): The set of Measurement objects.
        serializer_class (MeasurementSerializer): The serializer class for Measurement.
        authentication_classes (list): The authentication classes required for this view.
        permission_classes (list): The permission classes required for this view.
    """

    queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
