import uuid

from django.db import models
from django.utils import timezone
from django.utils.text import gettext_lazy as _


class TimeStampedModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Item(TimeStampedModel):
    desc = models.CharField(verbose_name=_("Item Description"), max_length=255, blank=False, null=False)
    hsn_code = models.CharField(verbose_name=_("HSN Code"), max_length=10, blank=False, null=False)
    gst_rate = models.PositiveIntegerField(verbose_name=_("GST Rate"))

    def __str__(self):
        return f"{self.desc}"

    class Meta:
        ordering = ["-created_at"]


class Invoice(TimeStampedModel):
    name = models.CharField(verbose_name=_("Customer Name"), max_length=255, blank=False, null=False)
    address = models.TextField(verbose_name=_("Customer Address"), null=True, blank=True)
    gst_number = models.CharField(verbose_name=_("GST"), max_length=15, blank=True, null=True)
    date = models.DateField(verbose_name=_("Invoice Date"), default=timezone.now)
    # true if GST
    is_b2b = models.BooleanField(verbose_name=_("B2B"), default=False)
    subtotal = models.DecimalField(verbose_name=_("Subtotal"), max_digits=10, decimal_places=2, null=True)
    total_gst_amount = models.DecimalField(
        verbose_name=_("Total GST Amount"), max_digits=10, decimal_places=2, null=True
    )
    # total = subtotal + total_gst_amount
    total = models.DecimalField(verbose_name=_("Total"), max_digits=10, decimal_places=2, null=True)

    def __str__(self):
        return f"{self.name} - {self.date}"

    class Meta:
        ordering = ["-date"]
        indexes = [models.Index(fields=["date"])]


class InvoiceItem(TimeStampedModel):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name="items")
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="invoices")
    quantity = models.PositiveIntegerField(verbose_name=_("Quantity"), default=1)
    price = models.DecimalField(verbose_name=_("Price"), max_digits=10, decimal_places=2)
    igst = models.PositiveIntegerField(verbose_name=_("IGST Rate"), null=True, blank=True)
    igst_amount = models.DecimalField(
        verbose_name=_("IGST Amount"), max_digits=10, decimal_places=2, null=True, blank=True
    )
    sgst = models.PositiveIntegerField(verbose_name=_("SGST Rate"), null=True, blank=True)
    sgst_amount = models.DecimalField(
        verbose_name=_("SGST Amount"), max_digits=10, decimal_places=2, null=True, blank=True
    )
    cgst = models.PositiveIntegerField(verbose_name=_("CGST Rate"), null=True, blank=True)
    cgst_amount = models.DecimalField(
        verbose_name=_("CGST Amount"), max_digits=10, decimal_places=2, null=True, blank=True
    )
    # total gst
    gst_amount = models.DecimalField(verbose_name=_("GST Amount"), max_digits=10, decimal_places=2)
    # price * quantity
    subtotal = models.DecimalField(verbose_name=_("Subtotal"), max_digits=10, decimal_places=2)
    # subtotal + gst_amount
    total = models.DecimalField(verbose_name=_("Total"), max_digits=10, decimal_places=2)

    class Meta:
        ordering = ["-created_at"]
