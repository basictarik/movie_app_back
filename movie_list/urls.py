from django.conf.urls import url
from django.urls import path
from movie_list import views

urlpatterns = [
    url(r'^movies/$', views.movie_list),
    url(r'^movies/(?P<pk>[0-9]+)$', views.movie_rate),
    path('register', views.register),
    path('token', views.token),
    path('token/refresh', views.refresh_token),
    path('token/revoke', views.revoke_token),
]
