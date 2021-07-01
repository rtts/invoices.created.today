from cms.decorators import section_view
from cms.forms import ContactForm
from cms.views import SectionFormView, SectionView
from django.utils.translation import gettext_lazy as _

from invoices import forms


@section_view
class Text(SectionView):
    verbose_name = _("Text")
    fields = ["content"]
    template_name = "text.html"


@section_view
class Images(SectionView):
    verbose_name = _("Image(s)")
    fields = ["images"]
    template_name = "images.html"


@section_view
class Video(SectionView):
    verbose_name = _("Video")
    fields = ["video"]
    template_name = "video.html"


@section_view
class Button(SectionView):
    verbose_name = _("Button")
    fields = ["href"]
    template_name = "button.html"


@section_view
class NewInvoice(SectionFormView):
    verbose_name = _("New invoice")
    fields = []
    form_class = forms.InvoiceForm
    success_url = "/"
    template_name = "invoice_form.html"


@section_view
class Contact(SectionFormView):
    verbose_name = _("Contact")
    fields = []
    form_class = ContactForm
    success_url = "/thanks/"
    template_name = "contact.html"
