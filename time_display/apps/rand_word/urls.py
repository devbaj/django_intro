from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'_word$', views.index),
    url(r'_word/new$', views.new),
    url(r'_word/reset$', views.reset)
]