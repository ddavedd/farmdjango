from django.urls import re_path, include
from django.contrib import admin
#admin.autodiscover()

urlpatterns = [
    # Examples:
    # url(r'^$', 'farm.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    #url(r'^farm/', include('farm.urls')),
    re_path(r'^admin/', admin.site.urls),
    #url('^', include('django.contrib.auth.urls')),
]
