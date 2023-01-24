from decimal import Decimal

from django.conf import settings
from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from invoice.models import Invoice, InvoiceItem, Item


class ItemResource(resources.ModelResource):
    class Meta:
        model = Item
        fields = ["desc", "hsn_code", "gst_rate"]
        export_order = ["desc", "hsn_code", "gst_rate"]


@admin.register(Item)
class ItemAdmin(ImportExportModelAdmin):
    resource_classes = [ItemResource]

    list_display = ["desc", "hsn_code", "gst_rate"]
    list_filter = ["gst_rate"]
    search_fields = ["hsn_code"]


class ItemInline(admin.TabularInline):
    model = InvoiceItem
    exclude = ["igst", "igst_amount", "sgst", "sgst_amount", "cgst", "cgst_amount", "gst_amount", "subtotal", "total"]
    readonly_fields = [
        "igst",
        "igst_amount",
        "sgst",
        "sgst_amount",
        "cgst",
        "cgst_amount",
        "gst_amount",
        "subtotal",
        "total",
    ]
    extra = 1


class InvoiceResource(resources.ModelResource):
    class Meta:
        model = Invoice
        fields = ["name", "date", "subtotal", "total_gst_amount", "total"]
        export_order = ["name", "date", "subtotal", "total_gst_amount", "total"]


@admin.register(Invoice)
class InvoiceAdmin(ImportExportModelAdmin):
    resource_classes = [InvoiceResource]
    list_display = ["name", "date", "subtotal", "total_gst_amount", "total"]
    list_filter = ["date"]
    search_fields = ["name", "date"]
    ordering = ["-date"]
    date_hierarchy = "date"
    inlines = [ItemInline]
    readonly_fields = ["subtotal", "total_gst_amount", "total", "is_b2b"]

    def has_change_permission(self, request, obj=None):
        return False

    def save_model(self, request, obj: Invoice, form, change):
        if obj.gst_number:
            obj.is_b2b = True

        obj.subtotal = Decimal(0)
        obj.total_gst_amount = Decimal(0)
        obj.total = Decimal(0)
        super().save_model(request, obj, form, change)

    def save_related(self, request, form, formsets, change):
        instance: Invoice = form.instance
        for formset in formsets:
            for form in formset:
                item: Item = form.cleaned_data["item"]
                quantity: int = form.cleaned_data["quantity"]
                price = form.cleaned_data["price"]
                sub_total = quantity * price
                invoice_item: InvoiceItem = form.instance
                output, invoice_item = self._calculate_gst(instance, item, invoice_item, sub_total)
                instance.subtotal += output["subtotal"]
                instance.total_gst_amount += output["gst_amount"]
                instance.total += output["total"]
                invoice_item.save()
                if hasattr(formset, "new_objects"):
                    formset.new_objects.append(invoice_item)
                else:
                    formset.new_objects = [invoice_item]
                    formset.changed_objects = []
                    formset.deleted_objects = []

            instance.save()

    def _calculate_gst(self, instance: Invoice, item: Item, invoice_item: InvoiceItem, subtotal):
        if instance.is_b2b:
            if instance.gst_number[:2] != settings.SYSTEM_GST_NUMBER[:2]:
                igst_rate = item.gst_rate
                gst_amount = subtotal * item.gst_rate / 100
                invoice_item.igst = igst_rate
                invoice_item.igst_amount = gst_amount
        else:
            gst_amount = self._extracted_from__calculate_gst(item, subtotal, invoice_item)

        output = {
            "gst_amount": gst_amount,
            "subtotal": subtotal,
            "total": subtotal + gst_amount,
        }
        invoice_item.gst_amount = gst_amount
        invoice_item.subtotal = subtotal
        invoice_item.total = subtotal + gst_amount
        return output, invoice_item

    def _extracted_from__calculate_gst(self, item, subtotal, invoice_item):
        # calculate
        cgst_rate = int(item.gst_rate / 2)
        cgst_amount = subtotal * cgst_rate / 100
        sgst_rate = int(item.gst_rate / 2)
        sgst_amount = subtotal * sgst_rate / 100
        result = cgst_amount + sgst_amount

        # update
        invoice_item.cgst = cgst_rate
        invoice_item.cgst_amount = cgst_amount
        invoice_item.sgst = sgst_rate
        invoice_item.sgst_amount = sgst_amount

        return result
