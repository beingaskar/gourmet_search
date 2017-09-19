from django.conf.urls import url
from .views import *

urlpatterns = [

    url(r'^search/$', ReviewSearchAPI.as_view(), name="reviews_search"),
]