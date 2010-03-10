from django.conf import settings

def duplicate_transfer_id(ipn_obj):
    """Returns True if a record with this transaction id exists."""
    return ipn_obj._default_manager.filter(lr_transfer=ipn_obj.lr_transfer).count() > 0

def make_secret(form_instance, secret_fields=None):
    """
    Returns a secret for use in a EWP form or an IPN verification based on a
    selection of variables in params. Should only be used with SSL.
    """
    import hashlib
    
    # Build the secret with fields availible in both PaymentForm and the IPN. Order matters.
    if secret_fields is None:
        secret_fields = ['lr_paidto', 'lr_paidby', 'lr_store', 'lr_amnt', 'lr_transfer', 'lr_merchant_ref', '', 'lr_currency']

    concat_fields = []
    for name in secret_fields:
        data = ""
        if hasattr(form_instance, 'cleaned_data'):
            if name in form_instance.cleaned_data:
                data = unicode(form_instance.cleaned_data[name])
        else:
            # Initial data passed into the constructor overrides defaults.
            if name in form_instance.initial:
                data = unicode(form_instance.initial[name])
            elif name in form_instance.fields and form_instance.fields[name].initial is not None:
                data = unicode(form_instance.fields[name].initial)
        concat_fields.append(data)
    concat_fields.append(settings.LIBERTYRESERVE_SECRET)

    concat_data = ':'.join(concat_fields)
    secret = hashlib.sha256(concat_data).hexdigest()
    return secret.upper()

def check_secret(form_instance, secret):
    """
    Returns true if received `secret` matches expected secret for form_instance.
    Used to verify IPN.
    """
    return make_secret(form_instance) == secret
