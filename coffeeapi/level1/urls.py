from django.urls import path

from coffeeapi.level1 import views

urlpatterns = [
    path('order/read', views.read),
    path('order/create', views.create),
    path('order/delete', views.delete),
    path('order/update', views.update),
]
