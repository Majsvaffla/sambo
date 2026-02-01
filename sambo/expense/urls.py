from django.urls import path,register_converter

from . import views
from . import converters

register_converter(converters.ISODateConverter, "iso_date")

urlpatterns = [
    path("<uuid:bill_identifier>", views.bill, name="bill"),
    path("<uuid:bill_identifier>/<iso_date:settled_at>", views.bill, name="bill_settled_at"),
    path("<uuid:bill_identifier>/", views.expense, name="expense_create"),
    path("<uuid:bill_identifier>/<int:expense_pk>", views.expense, name="expense_change"),
]
