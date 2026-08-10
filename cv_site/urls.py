from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    # Ohjataan etusivun pyynnöt portfolio-sovelluksen URL-reiteille.
    path("", include("portfolio.urls")),
]
