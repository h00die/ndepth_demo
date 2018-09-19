from django.conf.urls import include, url

from . import views

urlpatterns = [
  url(r'^login/$', views.login_view, name='login'),
  url(r'^logout/$', views.logout_view, name='logout'),
  url(r'^create_backup$', views.create_backup, name='create_backup'),
  url(r'^queue_download/$', views.queue_download, name='queue_download'),
  url(r'^download/$', views.download, name='download'),
  url(r'^config/$', views.config_page, name='config_page'),
  url(r'^timezone/$', views.timezone, name='timezone'),
  url(r'^', views.home, name='home'),
]
