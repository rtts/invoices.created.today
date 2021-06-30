from django.contrib import admin

from . import models


@admin.register(models.Organization)
class OrganizationAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Journal)
class JournalAdmin(admin.ModelAdmin):
    pass


class LineAdmin(admin.StackedInline):
    model = models.Line
    min_num = 1
    extra = 0


@admin.register(models.Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    inlines = [LineAdmin]
