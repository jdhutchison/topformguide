from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'topformguide.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    # Static information pages
    url(r'^admin/', include(admin.site.urls)),
    url(r'^/?$^', 'topformguide.views.index'),


    url(r'^car/(\d+)$', 'topformguide.views.displayCar'),  # View one car

    # Viewing by group
    url(r'body/types$', 'topformguide.views.bodylist'),  # View all body types
    url(r'body/(\w+)$', 'topformguide.views.index'),  # View by body types
    url(r'body/(\w+)/(\w+)$', 'topformguide.views.index'),  # View by body type and make
    url(r'(\w+)', 'topformguide.views.index'),  # View by make
    url(r'(\w+)/(\w+)/(\d{4})$', 'topformguide.views.index'),  # View by make, model and year

    # Top 20 lists
    url(r'^top/make/(\w+)$', 'topformguide.views.index'),  # Top 20 by make
    url(r'^top/bodytype/(\w+)$', 'topformguide.views.index')  # Top 20 by bodytype
)
