from django.http import HttpResponseRedirect
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^$', lambda r: HttpResponseRedirect('pollerapp/')),
    url(r'^pollerapp/', include('pollerapp.urls')),
    url(r'^admin/', admin.site.urls)
]
