from django.db import models
from django.conf import settings
from libertyreserve.helpers import duplicate_transfer_id, check_secret
from libertyreserve.signals import payment_was_successful, payment_was_flagged

class LibertyReserveIPN(models.Model):
    lr_paidto = models.CharField(max_length=8, blank=True)
    lr_paidby = models.CharField(max_length=8, blank=True)
    lr_amnt = models.DecimalField(max_digits=64, decimal_places=4, default=0, blank=True, null=True)
    lr_fee_amnt = models.DecimalField(max_digits=64, decimal_places=4, default=0, blank=True, null=True)
    lr_currency = models.CharField(max_length=5, blank=True)
    lr_transfer = models.CharField(max_length=64, blank=True, db_index=True)
    lr_store = models.CharField(max_length=50, blank=True)
    lr_timestamp = models.DateTimeField(blank=True, null=True)
    lr_merchant_ref = models.CharField(max_length=20, blank=True, db_index=True)

    lr_encrypted = models.CharField(max_length=64, blank=True)
    lr_encrypted2 = models.CharField(max_length=64, blank=True)

    ipaddress = models.IPAddressField(blank=True)
    flag = models.BooleanField(default=False, blank=True)
    flag_info = models.TextField(blank=True)
    query = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "IPN: Transaction %s" % self.lr_transfer

    def initialize(self, request):
        self.query = getattr(request, request.method).urlencode()
        self.ipaddress = request.META.get('REMOTE_ADDR', '')

    def set_flag(self, info):
        """Sets a flag on the transaction and also sets a reason."""
        self.flag = True
        self.flag_info += info

    def verify(self, form, item_check_callable=None):
        if duplicate_transfer_id(self):
            self.set_flag("Duplicate lr_transfer. (%s)" % self.lr_transfer)
        elif self.lr_paidto != settings.LIBERTYRESERVE_ACCOUNT:
            self.set_flag("Invalid lr_paidto. (%s)" % self.lr_paidto)
        elif not check_secret(form, self.lr_encrypted2):
            self.set_flag("Invalid lr_encrypted2. (%s)" % self.lr_encrypted2)
        elif callable(item_check_callable):
            flag, reason = item_check_callable(self)
            if flag:
                self.set_flag(reason)

        self.save()
        self.send_signals()

    def send_signals(self):
        """Shout for the world to hear whether a txn was successful."""
        if self.flag:
            payment_was_flagged.send(sender=self)
        else:
            payment_was_successful.send(sender=self)
    
