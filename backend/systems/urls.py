# urls.py

from django.urls import path
from .views import (
    HydroponicSystemList,
    HydroponicSystemDetail,
    MeasurementListCreate,
    MeasurementDetail,
)

urlpatterns = [
    path(
        "hydroponic-systems/",
        HydroponicSystemList.as_view(),
        name="hydroponic-system-list",
    ),
    path(
        "hydroponic-systems/<int:pk>/",
        HydroponicSystemDetail.as_view(),
        name="hydroponic-system-detail",
    ),
    path(
        "measurements/", MeasurementListCreate.as_view(), name="measurement-list-create"
    ),
    path(
        "measurements/<int:pk>/", MeasurementDetail.as_view(), name="measurement-detail"
    ),
]
