from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
#from .views import SearchResults


urlpatterns = [
    path('', views.about, name='about'),
    path('recommend/', views.recommend, name='recommend'),
    path('items/', views.items, name='items'),
    path('search/', views.search, name='search'),
    #path('login-successful/', views.home, name='login-successful'),
    #path('search/', SearchResults.as_view(), name='search_results')
]


