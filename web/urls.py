from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('web.views',
    (r'^$', "contour_form"),
    (r'^show_all/$', "contour_show_all"),
    (r'^show_one/$', "contour_show_one"),
)
