from django.views import generic

from . import models


class InvoiceDetail(generic.DetailView):
    model = models.Invoice
    slug_field = "uuid"
    slug_url_kwarg = "uuid"
