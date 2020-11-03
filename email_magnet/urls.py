from django.urls import path, include
from . import views


app_name = 'email_magnet'
urlpatterns = [
    path('', views.index, name='index'),
    path('detail_search', views.detail_search, name='detail_search'),
    path('brute_force', views.brute_search, name='brute_search'),
    path('signup/', views.sign_up, name='signup')

]