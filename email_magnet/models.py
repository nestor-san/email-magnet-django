from django.db import models
from django.conf import settings
from email_magnet.scripts import detailed_search

# Create your models here.
class DetailSearch(models.Model):
    domain = models.CharField(max_length=40, verbose_name="Domain name", help_text="The domain name of the company that you're targetting. *This is a required field.")
    first_name = models.CharField(max_length=30, blank=True, verbose_name="First name", help_text="The first name of employer at the company that you're targetting. It is recommended to fill in this field")
    middle_name = models.CharField(max_length=30, blank=True, verbose_name="Middle name", help_text="The middle name of employer at the company that you're targetting. You can leave it blank.")
    last_name = models.CharField(max_length=30, blank=True, verbose_name="Last name", help_text="The last name of employer at the company that you're targetting. It is recommended to fill in this field")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    possible_emails = models.TextField(null=True)
    valid_emails = models.TextField(null=True)

    def __str__(self):
        name = 'Search for {} {} {} at {}'.format(self.first_name, self.middle_name, self.last_name, self.domain)
        return name
    

    def get_valid_email(self):
        emails = detailed_search.detailed_search(self.domain, self.first_name, self.middle_name, self.last_name)
        return emails
