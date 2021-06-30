from django.urls import path

from . import views

app_name = "invoices"

urlpatterns = [
    path("<uuid:uuid>/", views.InvoiceDetail.as_view(), name="invoice_detail"),
]
