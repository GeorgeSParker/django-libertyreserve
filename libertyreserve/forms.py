from django import forms
from django.utils.safestring import mark_safe
from models import LibertyReserveIPN
from conf import POSTBACK_ENDPOINT

# Yes, YYYY-DD-MM according to the LR specs.
LIBERTYRESERVE_DATE_FORMAT = ('%Y-%d-%m %H:%M:%S',)

class ValueHiddenInput(forms.HiddenInput):
    """
    Widget that renders only if it has a value.
    Used to remove unused fields from form.
    """
    def render(self, name, value, attrs=None):
        if value is None:
            return u''
        else:
            return super(ValueHiddenInput, self).render(name, value, attrs)

class LibertyReservePaymentsForm(forms.Form):
    """
    Form to generate 'Pay with Liberty Reserve' button.
    When using, be sure to disable the CSRF token in the generated form.
    """
    lr_acc = forms.CharField(widget=ValueHiddenInput())
    lr_store = forms.CharField(widget=ValueHiddenInput())
    lr_amnt = forms.CharField(widget=ValueHiddenInput())
    lr_currency = forms.CharField(widget=ValueHiddenInput())
    lr_comments = forms.CharField(widget=ValueHiddenInput())
    lr_merchant_ref = forms.CharField(widget=ValueHiddenInput())
    lr_success_url = forms.CharField(widget=ValueHiddenInput())
    lr_success_url_method = forms.CharField(widget=ValueHiddenInput())
    lr_fail_url = forms.CharField(widget=ValueHiddenInput())
    lr_fail_url_method = forms.CharField(widget=ValueHiddenInput())
    lr_status_url = forms.CharField(widget=ValueHiddenInput())
    lr_status_url_method = forms.CharField(widget=ValueHiddenInput())

    def render(self):
        return mark_safe(u"""<form action="%s" method="post">
    %s
    <input type="submit" value="Pay with Liberty Reserve" />
</form>""" % (POSTBACK_ENDPOINT, self.as_p()))

class LibertyReserveIPNForm(forms.ModelForm):
    class Meta:
        model = LibertyReserveIPN

    lr_timestamp = forms.DateTimeField(required=False, input_formats=LIBERTYRESERVE_DATE_FORMAT)

