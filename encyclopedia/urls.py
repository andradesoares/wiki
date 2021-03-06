from django.urls import path

from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry>", views.entry, name="entry"),
    path("new", views.new, name="new"),
    path("edit", views.edit, name="edit"),
    path("search", views.search, name="search"),
    path("random/", views.random_page, name="random_page"),
]
