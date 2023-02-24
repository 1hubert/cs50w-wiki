from django.urls import path

from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("wiki/<str:entry_title>/edit/", views.edit, name="edit"),
    path("wiki/<str:entry_title>/", views.entry, name="entry"),
    path("", views.index, name="index"),
    path("new/", views.new, name="new"),
    path("random/", views.rand, name="rand"),
    path("search/", views.search, name="search")
]
