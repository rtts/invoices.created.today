# Generated by Django 3.2.4 on 2021-06-30 19:50

import uuid

import cms.fields
import cms.mixins
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Invoice",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "uuid",
                    models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
                ),
                ("language", cms.fields.CharField(default="nl")),
                ("recipient", cms.fields.TextField()),
                ("number", cms.fields.PositiveIntegerField(null=True)),
                ("date", cms.fields.DateField(null=True)),
            ],
            options={
                "verbose_name": "invoice",
                "verbose_name_plural": "invoices",
                "ordering": ["number"],
            },
        ),
        migrations.CreateModel(
            name="Organization",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "uuid",
                    models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
                ),
                ("name", cms.fields.SlugField(unique=True)),
                ("users", cms.fields.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                "verbose_name": "organization",
                "verbose_name_plural": "organizations",
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="Line",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "uuid",
                    models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
                ),
                ("number", cms.fields.PositiveIntegerField()),
                ("description", cms.fields.TextField()),
                (
                    "quantity",
                    cms.fields.DecimalField(decimal_places=2, default=1, max_digits=10),
                ),
                ("unit", cms.fields.CharField(default="hours")),
                (
                    "unit_price",
                    cms.fields.DecimalField(decimal_places=2, max_digits=10),
                ),
                (
                    "vat_percentage",
                    cms.fields.DecimalField(decimal_places=2, max_digits=5),
                ),
                ("date", cms.fields.DateField(null=True)),
                (
                    "invoice",
                    cms.fields.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="invoices.invoice",
                    ),
                ),
            ],
            options={
                "verbose_name": "line",
                "verbose_name_plural": "lines",
                "ordering": ["number"],
            },
            bases=(cms.mixins.Numbered, models.Model),
        ),
        migrations.CreateModel(
            name="Journal",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "uuid",
                    models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
                ),
                ("name", cms.fields.SlugField(default="default")),
                ("number_format", cms.fields.CharField(default="%Y{number:04d}")),
                ("last_number", cms.fields.PositiveIntegerField(default=1)),
                ("template", cms.fields.TextField(default="TODO")),
                (
                    "organization",
                    cms.fields.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="invoices.organization",
                    ),
                ),
            ],
            options={
                "verbose_name": "journal",
                "verbose_name_plural": "journals",
                "ordering": ["name"],
                "unique_together": {("organization", "name")},
            },
        ),
        migrations.AddField(
            model_name="invoice",
            name="journal",
            field=cms.fields.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="invoices.journal"
            ),
        ),
        migrations.AlterUniqueTogether(
            name="invoice",
            unique_together={("journal", "number")},
        ),
    ]
