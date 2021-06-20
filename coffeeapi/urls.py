from django.urls import include, path

urlpatterns = [
    path('', include('coffeeapi.level0.urls')),
    path('', include('coffeeapi.level1.urls')),
    path('', include('coffeeapi.level3.urls')),
    path('', include('coffeeapi.level2.urls')),
]
