from django.conf.urls import url 
from api import views 
 
urlpatterns = [ 
    url(r'^api/api$', views.text_list),
    url(r'^api/api/(?P<pk>[0-9]+)$', views.text_detail),
    url(r'^api/api/published$', views.text_list_published)
]