from django.conf.urls import  url
from sign import  views_if, views_if_sec

app_name='[sign]'
urlpatterns = [
    url(r'^add_event/', views_if.add_event, name='add_event'),
    url(r'^add_guest/', views_if.add_guest, name='add_guest'),
    url(r'^get_event_list/', views_if.get_event_list, name="get_event_list"),
    url(r'^get_guest_list/', views_if.get_guest_list, name="get_guest_list"),
    url(r'^user_sign/', views_if.user_sign, name='user_sign'),
    url(r'^sec_add_event', views_if_sec.sec_add_event, name='sec_add_event'),
    url(r'^md5_add_event', views_if_sec.md5_add_event, name='md5_add_event'),
]