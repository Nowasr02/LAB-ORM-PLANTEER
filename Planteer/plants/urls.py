from django.urls import path
from . import views

app_name = "plants"

urlpatterns = [
    path("add/plant", views.add_plant_view, name="add_plant_view"),
    path("all/plants", views.all_plants_view, name="all_plants_view"),
    path("details/<int:plant_id>/", views.plant_details_view, name="plant_details_view"),
    path("update/<int:plant_id>/", views.update_plant_view, name="update_plant_view"),
    path("delete/<int:plant_id>/", views.delete_plant_view, name="delete_plant_view"),
    path("search/", views.search_view, name="search_view"),
    path("add/reviews/<int:plant_id>/", views.add_review_view, name="add_review_view"),

]