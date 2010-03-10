from django.conf.urls.defaults import patterns, url
 
urlpatterns = patterns('libertyreserve.views',
    url(r'^$', 'ipn', name="libertyreserve-ipn"),
)
