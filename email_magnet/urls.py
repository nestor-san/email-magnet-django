from django.urls import path
from . import views

# Define an app name, as good practices
app_name = 'email_magnet'

# Define the patterns of the urls and the view related
urlpatterns = [
    path('', views.index, name='index'),  # Homepage / index url
    # Detail Search url
    path('detail_search', views.detail_search, name='detail_search'),
    # Brute force search url
    path('brute_force', views.brute_search, name='brute_search'),
    path('signup/', views.sign_up, name='signup'),  # Sign Up url
    # Detailed results url (list of all detailed searches from user)
    path('detailed_results', views.detailed_results, name='detailed_results'),
    # Detailed search url (single detail search)
    path('detailed_results/<int:search_pk>',
         views.detailed_search_detail,
         name='detailed_search_detail'),
    # Delete a single search by ID
    path('detailed_results/<int:search_pk>/delete',
         views.delete_search,
         name='delete_search'),
    # Export the detail search data url
    path('export', views.export_data, name='export_data'),
]
