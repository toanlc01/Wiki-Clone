from django.urls import path

from . import views


app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<TITLE>", views.entryPage, name="entryPage"),
    path("search", views.search, name="search")
]
