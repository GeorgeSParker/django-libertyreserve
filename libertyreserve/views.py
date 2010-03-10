from django.http import HttpResponse
from django.contrib.csrf.middleware import csrf_exempt
from django.views.decorators.http import require_POST
from forms import LibertyReserveIPNForm
from models import LibertyReserveIPN

@csrf_exempt
@require_POST
def ipn(request, item_check_callable=None):
    flag = None
    ipn_obj = None
    form = LibertyReserveIPNForm(request.POST)
    if form.is_valid():
        try:
            ipn_obj = form.save(commit=False)
        except Exception, e:
            flag = "Exception while processing. (%s)" % e
    else:
        flag = "Invalid form. (%s)" % form.errors
 
    if ipn_obj is None:
        ipn_obj = LibertyReserveIPN()
 
    ipn_obj.initialize(request)
 
    if flag is not None:
        ipn_obj.set_flag(flag)
    else:
        ipn_obj.verify(form, item_check_callable)
 
    ipn_obj.save()
    return HttpResponse("OKAY")
