from django.urls import path
from . import views

app_name = "countries"

urlpatterns = [
    path("add/", views.add_country, name="add_country"),
    path("all/", views.countries_view, name="countries_view"),
    path("<country_id>/", views.country_view, name="country_view"),
]