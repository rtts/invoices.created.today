import uuid
from decimal import Decimal

from cms import fields, mixins, models
from django.conf import settings
from django.db import transaction
from django.db.models import CASCADE, UUIDField
from django.shortcuts import reverse
from django.utils import timezone
from django.utils.translation import gettext
from django.utils.translation import gettext_lazy as _


class BaseModel(models.Model):
    uuid = UUIDField(
        unique=True,
        default=uuid.uuid4,
        editable=False,
    )

    class Meta:
        abstract = True


class Organization(BaseModel):
    """
    An organization that sends out invoices.
    """

    name = fields.SlugField(_("name"), unique=True)
    users = fields.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)

    class Meta:
        verbose_name = _("organization")
        verbose_name_plural = _("organizations")
        ordering = ["name"]

    def __str__(self):
        return self.name


class Journal(BaseModel):
    """
    A collection of invoices that look the same.
    """

    organization = fields.ForeignKey(
        Organization,
        verbose_name=_("organization"),
        on_delete=CASCADE,
        related_name="journals",
    )
    name = fields.SlugField(_("name"), default=_("default"))
    number_format = fields.CharField(_("number format"), default="%Y{number:04d}")
    last_number = fields.PositiveIntegerField(_("last number"), default=1)
    template = fields.TextField(_("template"), default="TODO")

    class Meta:
        verbose_name = _("journal")
        verbose_name_plural = _("journals")
        ordering = ["name"]
        unique_together = ["organization", "name"]

    def __str__(self):
        return self.name


class Invoice(BaseModel):
    """
    An invoice that should not be edited after it’s finalized.
    """

    journal = fields.ForeignKey(
        Journal,
        verbose_name=_("journal"),
        on_delete=CASCADE,
        related_name="invoices",
    )
    language = fields.CharField(
        _("language"), choices=settings.LANGUAGES, default=settings.LANGUAGE_CODE
    )
    currency = fields.CharField(_("currency"), default="€")
    recipient = fields.TextField(_("recipient"))
    number = fields.PositiveIntegerField(_("number"), blank=True, null=True)
    date = fields.DateField(_("date"), blank=True, null=True)

    class Meta:
        verbose_name = _("invoice")
        verbose_name_plural = _("invoices")
        ordering = ["number"]
        unique_together = ["journal", "number"]

    def __str__(self):
        return self.format_number()

    def get_absolute_url(self):
        return reverse("invoices:invoice_detail", args=[self.uuid])

    @property
    def final(self):
        return self.number is not None

    @property
    def total(self):
        return sum([line.total for line in self.lines])

    def finalize(self):
        self.date = timezone.now()
        self.number = self.journal.last_number + 1
        self.journal.last_number = self.number
        with transaction.atomic():
            self.journal.save()
            self.save()

    def format_number(self):
        # TODO
        return self.number or gettext("draft")


class Line(mixins.Numbered, BaseModel):
    """
    An invoice line.
    """

    invoice = fields.ForeignKey(
        Invoice,
        verbose_name=_("invoice"),
        on_delete=CASCADE,
        related_name="lines",
    )
    number = fields.PositiveIntegerField(_("number"), blank=True)
    description = fields.TextField(_("description"))
    quantity = fields.DecimalField(
        _("Quantity"), max_digits=10, decimal_places=2, default=1
    )
    unit = fields.CharField(_("unit"), default=_("hours"))
    unit_price = fields.DecimalField(_("unit price"), max_digits=10, decimal_places=2)
    vat_percentage = fields.DecimalField(
        _("VAT percentage"), max_digits=5, decimal_places=2
    )
    date = fields.DateField(_("date"), blank=True, null=True)

    class Meta:
        verbose_name = _("line")
        verbose_name_plural = _("lines")
        ordering = ["number"]

    def __str__(self):
        return f"#{self.number}"

    def number_with_respect_to(self):
        return self.invoice.lines.all()

    @property
    def total(self):
        return (self.unit_price * self.quantity).quantize(Decimal("0.01"))
