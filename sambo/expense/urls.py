from django.urls import path, register_converter

from . import converters, views

register_converter(converters.ISODateConverter, "iso_date")

urlpatterns = [
    path("<uuid:bill_identifier>", views.bill, name="bill"),
    path("<uuid:bill_identifier>/expense", views.expense, name="expense_create"),
    path("<uuid:bill_identifier>/expense/<int:expense_pk>", views.expense, name="expense_edit"),
]
