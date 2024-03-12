from django.urls import path, include, re_path
from django.contrib import admin
from rest_framework import routers
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Hydroponic System API",
        default_version="v1",
        description="API documentation for Hydroponic System",
    ),
    public=True,
)

router = routers.DefaultRouter()

urlpatterns = router.urls

urlpatterns += [
    path("admin/", admin.site.urls),
    path("user/", include("core.urls")),
    path("systems/", include("systems.urls")),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]
