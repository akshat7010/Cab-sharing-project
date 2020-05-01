from django.urls import path
from . import views
from django.conf.urls import url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

app_name='cabs'


urlpatterns=[
    url(r'^$',views.index,name='main'),
    url(r'^post/$', views.post_view, name='post'),
    url(r'^signup/$', views.signup_view, name='signup'),
    url(r'^login/$', views.login_view, name='login'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^bookings/$', views.booking_view, name='bookings'),
    path('bookings/<int:id>/cancel', views.cancel_view, name='cancel'),
    url(r'^notifications/$', views.notification_view, name='notifications'),
    url(r'^aboutus/$', views.aboutus_view, name='aboutus'),
    url(r'^feedback/$', views.feedback_view, name='feedback'),
    url(r'^contact/$', views.contact_view, name='contact'),
    path('brequest/<name1>/<name2>/<int:id>', views.request_view, name='brequest'),
    url(r'^requestpage/$', views.requestpage_view, name='requestpage'),
    path('requestpage/<int:id>/Rcancel', views.Rcancel_view, name='Rcancel'),
    path('Fgroup2/<int:bid>/<name1>/<name2>/<int:rid>', views.Fgroup2_view, name='Fgroup2'),
    url(r'^groups/$', views.groups_view, name='groups'),
    path('groups/<int:id>/Gcancel', views.Gcancel_view, name='Gcancel'),
]

urlpatterns+=staticfiles_urlpatterns()