from django.conf.urls.defaults import patterns, url
 
urlpatterns = patterns('libertyreserve.ipn.views',
    url(r'^$', 'ipn', name="libertyreserve-ipn"),
)
