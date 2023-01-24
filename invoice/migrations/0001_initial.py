# Generated by Django 4.1.5 on 2023-01-24 09:20

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Invoice",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("modified_at", models.DateTimeField(auto_now=True)),
                (
                    "name",
                    models.CharField(max_length=255, verbose_name="Customer Name"),
                ),
                (
                    "address",
                    models.TextField(
                        blank=True, null=True, verbose_name="Customer Address"
                    ),
                ),
                (
                    "gst_number",
                    models.CharField(
                        blank=True, max_length=15, null=True, verbose_name="GST"
                    ),
                ),
                (
                    "date",
                    models.DateField(
                        default=django.utils.timezone.now, verbose_name="Invoice Date"
                    ),
                ),
                ("is_b2b", models.BooleanField(default=False, verbose_name="B2B")),
                (
                    "subtotal",
                    models.DecimalField(
                        decimal_places=2, max_digits=10, verbose_name="Subtotal"
                    ),
                ),
                (
                    "total_gst_amount",
                    models.DecimalField(
                        decimal_places=2, max_digits=10, verbose_name="Total GST Amount"
                    ),
                ),
                (
                    "total",
                    models.DecimalField(
                        decimal_places=2, max_digits=10, verbose_name="Total"
                    ),
                ),
            ],
            options={
                "ordering": ["-date"],
            },
        ),
        migrations.CreateModel(
            name="Item",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("modified_at", models.DateTimeField(auto_now=True)),
                (
                    "desc",
                    models.CharField(max_length=255, verbose_name="Item Description"),
                ),
                ("hsn_code", models.CharField(max_length=10, verbose_name="HSN Code")),
                ("gst_rate", models.PositiveIntegerField(verbose_name="GST Rate")),
            ],
            options={
                "ordering": ["-created_at"],
            },
        ),
        migrations.CreateModel(
            name="InvoiceItem",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("modified_at", models.DateTimeField(auto_now=True)),
                (
                    "quantity",
                    models.PositiveIntegerField(default=1, verbose_name="Quantity"),
                ),
                (
                    "price",
                    models.DecimalField(
                        decimal_places=2, max_digits=10, verbose_name="Price"
                    ),
                ),
                ("igst", models.PositiveIntegerField(verbose_name="IGST Rate")),
                (
                    "igst_amount",
                    models.DecimalField(
                        decimal_places=2, max_digits=10, verbose_name="IGST Amount"
                    ),
                ),
                ("sgst", models.PositiveIntegerField(verbose_name="SGST Rate")),
                (
                    "sgst_amount",
                    models.DecimalField(
                        decimal_places=2, max_digits=10, verbose_name="SGST Amount"
                    ),
                ),
                ("cgst", models.PositiveIntegerField(verbose_name="CGST Rate")),
                (
                    "cgst_amount",
                    models.DecimalField(
                        decimal_places=2, max_digits=10, verbose_name="CGST Amount"
                    ),
                ),
                (
                    "gst_amount",
                    models.DecimalField(
                        decimal_places=2, max_digits=10, verbose_name="GST Amount"
                    ),
                ),
                (
                    "subtotal",
                    models.DecimalField(
                        decimal_places=2, max_digits=10, verbose_name="Subtotal"
                    ),
                ),
                (
                    "total",
                    models.DecimalField(
                        decimal_places=2, max_digits=10, verbose_name="Total"
                    ),
                ),
                (
                    "invoice",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="items",
                        to="invoice.invoice",
                    ),
                ),
                (
                    "item",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="invoices",
                        to="invoice.item",
                    ),
                ),
            ],
            options={
                "ordering": ["-created_at"],
            },
        ),
        migrations.AddIndex(
            model_name="invoice",
            index=models.Index(fields=["date"], name="invoice_inv_date_6c372c_idx"),
        ),
    ]