from django.conf.urls import patterns, url
from crimeapp import views

urlpatterns = patterns(
    'crimeapp.views',
    url(r'^$', views.recent, name='recent'),
)
