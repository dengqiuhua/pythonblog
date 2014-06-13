from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    # url(r'^$', 'pynews.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
   
    #url(r'^/static/$', 'static'),
    url(r'^$', 'blog.views.index'),
    url(r'^new/$', 'blog.views.new'),
    url(r'^new/art_(\d{1,2})$', 'blog.views.new'),
    url(r'^art_(\d{1,2})/$', 'blog.views.show'),
    url(r'^u/(\w+)/$', 'blog.views.home'),
    url(r'^p_(\d{1,2})/$', 'blog.views.index'),
    url(r'^delete/art_(\d{1,2})/$', 'blog.views.delete'),
    url(r'^login/$', 'blog.views.login'),
    url(r'^regester/$', 'blog.views.regester'),
    url(r'^loginout/$', 'blog.views.loginout'),
]
