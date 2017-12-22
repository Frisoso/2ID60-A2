from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    url(r'^$', views.HomePage.as_view(), name='liqorice_home'),
    url(r'^comments/$', views.CommentList.as_view()),
    url(r'^comments/(?P<id>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})/$', views.CommentDetail.as_view()),
    url(r'^users/$', views.UserList.as_view()),
    url(r'^users/(?P<id>[0-9]+)/$', views.UserDetail.as_view()),
    url(r'^login/$', views.custom_login, name='login'),
    url(r'^logout/$', views.custom_logout, name='logout', kwargs={'next_page': '/'}),

]

urlpatterns = format_suffix_patterns(urlpatterns)
