from django.db import models
from django.contrib.auth.models import User


class HydroponicSystem(models.Model):
    """
    Model representing a hydroponic system.

    Attributes:
        owner (User): The user who owns the hydroponic system.
        name (str): The name of the hydroponic system.
        description (str, optional): A description of the hydroponic system (optional).

    Methods:
        __str__: String representation of the hydroponic system.
    """

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        """
        String representation of the hydroponic system.

        Returns:
            str: The name of the hydroponic system.
        """
        return self.name


class Measurement(models.Model):
    """
    Model representing a measurement in a hydroponic system.

    Attributes:
        system (HydroponicSystem): The hydroponic system to which the measurement belongs.
        data (datetime): The date and time when the measurement was recorded.
        ph (float): The pH value of the measurement.
        temperature_raw (str): The raw temperature value as recorded.
        tds (float): The Total Dissolved Solids (TDS) value of the measurement.

    Methods:
        __str__: String representation of the measurement.
    """

    system = models.ForeignKey(
        HydroponicSystem, related_name="measurements", on_delete=models.CASCADE
    )
    data = models.DateTimeField(auto_now_add=True)
    ph = models.FloatField()
    temperature_raw = models.CharField(max_length=10)
    tds = models.FloatField()

    def __str__(self):
        """
        String representation of the measurement.

        Returns:
            str: The string representation of the measurement.
        """
        return f"Measurement for {self.system.name} - {self.data}"
