from django.urls import path

from . import views
from .views import NewEntryFormView
app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry_title>", views.entry, name="entry"),
    path("new/", NewEntryFormView.as_view(), name="new"),
    path("random/", views.rand, name="rand")
]
