import requests
from email_magnet.models import DetailSearch

def my_cron_job():
    pending_search = DetailSearch.objects.filter(valid_emails=None)
    for search in pending_search:
        search.get_valid_email()
        search.save()

