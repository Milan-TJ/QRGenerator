from django.urls import path
from . import views

app_name = "generator"
urlpatterns = [
    path("", views.index, name="index"),
    path("doc", views.info, name="index"),
    path("api/generate-png/", views.api_generate_png, name="api_generate_png"),
]
