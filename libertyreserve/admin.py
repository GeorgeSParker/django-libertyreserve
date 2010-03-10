from django.contrib import admin
from libertyreserve.models import LibertyReserveIPN
 
 
class LibertyReserveIPNAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_at'
    fieldsets = (
        (None, {
            "fields": [
                "flag", "lr_transfer", "lr_merchant_ref", "lr_currency",
                "lr_amnt", "lr_fee_amnt", "lr_timestamp"
            ]
        }),
        ("Buyer", {
            "description": "The information about the Buyer.",
            'classes': ('collapse',),
            "fields": [
                "lr_paidby"
            ]
        }),
        ("Seller", {
            "description": "The information about the Seller.",
            'classes': ('collapse',),
            "fields": [
                "lr_paidto", "lr_store"
            ]
        }),
        ("Admin", {
            "description": "Additional Info.",
            "classes": ('collapse',),
            "fields": [
                "ipaddress", "query", "flag_info"
            ]
        }),
    )
    list_display = [
        "__unicode__", "flag", "flag_info", "created_at"
    ]
    search_fields = ["lr_transfer", "lr_merchant_ref"]
 
 
admin.site.register(LibertyReserveIPN, LibertyReserveIPNAdmin)
