from django.urls import path, re_path

from coffeeapi.level2 import views

urlpatterns = [
    re_path(r'order(?:/(?P<id>\d+))?', views.dispatch, name='order'),
    #path('order', views.dispatch),
]
