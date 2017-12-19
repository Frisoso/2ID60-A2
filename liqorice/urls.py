from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    url(r'^$', views.HomePage.as_view(), name='liqorice_home'),
    url(r'^comments/$', views.CommentList.as_view()),
    url(r'^comments/(?P<id>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})/$', views.CommentDetail.as_view()),
    url(r'^comments/new/$', views.CommentNew.as_view(), name='new_comment'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
