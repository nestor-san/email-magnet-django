from django.urls import path, include
from . import views


app_name = 'email_magnet'
urlpatterns = [
    path('', views.index, name='index'),
    path('detail_search', views.detail_search, name='detail_search'),
    path('brute_force', views.brute_search, name='brute_search'),
    path('signup/', views.sign_up, name='signup'),
    path('detailed_results', views.detailed_results, name='detailed_results'),
    path('detailed_results/<int:search_pk>', views.detailed_search_detail, name='detailed_search_detail'),
    path('detailed_results/<int:search_pk>/delete', views.delete_search, name='delete_search'),

]