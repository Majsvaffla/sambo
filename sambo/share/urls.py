from django.urls import path

from . import views

urlpatterns = [
    path("", views.upload, name="upload"),
    path("<uuid:upload_identifier>", views.uploaded, name="uploaded"),
    path("<uuid:upload_identifier>/download", views.download, name="download"),
]
