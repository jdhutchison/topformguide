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
    url(r'^body/types$', 'topformguide.views.bodylist'),  # View all body types
    url(r'^body/(?P<filter>\w+)$', 'topformguide.views.showMakes', {'type': 'body'}),  # View by body types
    url(r'^body/(\w+)/(\w+)$', 'topformguide.views.showVariantsForBodyTypeAndMake'),  # View by body type and make

    # View by make, model and year
    url(r'^cars$', 'topformguide.views.showMakes'),  # View models
    url(r'^cars/([\w\-]+)$', 'topformguide.views.showModelsForMake'),  # View models by make
    url(r'^cars/([\w\-]+)/([\w\-]+)$', 'topformguide.views.variantsForMakeAndModel'),  # View by make, model
    url(r'^cars/([\w\-]+)/([\w\-]+)/(\d{4})$', 'topformguide.views.variantsForMakeAndModel'),
    # View by make, model and year

    # Top 20 lists
    url(r'^top/make$', 'topformguide.views.showMakes', {'type': 'rating', 'filter': None}),
    url(r'^top/bodytype$', 'topformguide.views.topBodyTypes'),  # Top 20 by bodytype
    url(r'^top/fueltype$', 'topformguide.views.topFuelTypes'),  # Top 20 by bodytype
    url(r'^top/make/(?P<type>[\w\-]+)$', 'topformguide.views.getTopVariantsForType', {'listType': 'make'}),
    # Top 20 by make
    url(r'^top/fueltype/(?P<type>[\w\-]+)$', 'topformguide.views.getTopVariantsForType', {'listType': 'fuel'}),
    # Top 20 by make
    url(r'^top/bodytype/(?P<type>[\w\-]+)$', 'topformguide.views.getTopVariantsForType', {'listType': 'body'})
    # Top 20 by bodytype
)
