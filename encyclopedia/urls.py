from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search/", views.search, name="search"),
    path("create", views.save, name = "save"),
    path("create", views.create, name = "create"),
    path("random", views.rand, name = "random"),
    path("<str:title>", views.load_entry, name="entry"),
    path("<str:title>/edit", views.edit, name="edit"),
    
    
]

