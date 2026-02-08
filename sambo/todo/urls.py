from django.urls import path

from . import views

urlpatterns = [
    path("", views.check_list, name="check_list_create"),
    path("<uuid:list_identifier>", views.check_list, name="check_list"),
    path("<uuid:list_identifier>/<int:item_pk>", views.check_list_item, name="check_list_item"),
]
