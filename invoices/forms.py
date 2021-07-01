from django import forms

from invoices import models


class InvoiceForm(forms.ModelForm):
    class Meta:
        model = models.Invoice
        fields = ["language", "currency", "recipient"]
