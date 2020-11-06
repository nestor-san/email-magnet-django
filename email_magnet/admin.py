from django.contrib import admin
from email_magnet.models import DetailSearch, BruteForceSearch

# Register your models here.
admin.site.register(DetailSearch) #Register Detail Search model
admin.site.register(BruteForceSearch) #Register Brute Force Search model