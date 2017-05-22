from django.conf.urls import url
from . import views

urlpatterns = [
    url(u'^$', views.index, name='index'),
    url(u'^analysis$', views.analysis, name='analysis'),
    url(u'^upload_file$', views.upload_file, name='upload_file')
]