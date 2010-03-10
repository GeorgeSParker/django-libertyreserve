from django.conf.urls.defaults import patterns

def verify_custom(ipn_obj):
    """Custom verifier that checks amount and currency"""
    import decimal
    if ipn_obj.lr_amnt != decimal.Decimal('12.34'):
        return (True, 'Invalid lr_amnt. (%s)' % ipn_obj.lr_amnt)
    if ipn_obj.lr_currency != 'LRUSD':
        return (True, 'Invalid lr_currency. (%s)' % ipn_obj.lr_currency)
    return (False,'')

def fail_custom(ipn_obj):
    """Custom verifier that always fails"""
    return (True, 'Always failing.')
 
urlpatterns = patterns('libertyreserve.views',
    (r'^ipn/$', 'ipn'),
    (r'^ipn_verify_custom/$', 'ipn', {'item_check_callable': verify_custom}),
    (r'^ipn_fail_custom/$', 'ipn', {'item_check_callable': fail_custom}),
)


