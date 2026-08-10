from django.urls import path

from . import views


# Sovelluksen omat URL-reitit
urlpatterns = [
    # Tyhjä reitti tarkoittaa portfolio-sovelluksen etusivua.
    path("", views.home, name="home"),
]
