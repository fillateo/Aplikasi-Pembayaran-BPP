from django.conf.urls import url, include
from django.contrib import admin


urlpatterns = [
	url(r'^accounts/', include('accounts.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'', include('app_bpp.urls')),
]
