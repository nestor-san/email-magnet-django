from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.conf import settings
from email_magnet.scripts import detailed_search
from django.core.mail import send_mail

# Create your models here.
class DetailSearch(models.Model):
    domain = models.CharField(max_length=40, verbose_name="Domain name", help_text="The domain name of the company that you're targetting. *This is a required field.")
    first_name = models.CharField(max_length=30, blank=True, verbose_name="First name", help_text="The first name of employer at the company that you're targetting. It is recommended to fill in this field")
    middle_name = models.CharField(max_length=30, blank=True, verbose_name="Middle name", help_text="The middle name of employer at the company that you're targetting. You can leave it blank.")
    last_name = models.CharField(max_length=30, blank=True, verbose_name="Last name", help_text="The last name of employer at the company that you're targetting. It is recommended to fill in this field")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    possible_emails = models.TextField(null=True)
    valid_emails = models.TextField(null=True)

    def __str__(self):
        name = 'Search for {} {} {} at {}'.format(self.first_name, self.middle_name, self.last_name, self.domain)
        return name
    
    #check if it's possible to find a valid email with the details provided(domain & first/middle/last name)
    def get_valid_email(self):
        emails = detailed_search.detailed_search(self.domain, self.first_name, self.middle_name, self.last_name)
        self.possible_emails = emails[0]
        self.valid_emails = emails[1]

    def notify_user(self):
        #Send email to the user with the results
        if self.valid_emails=='There are no valid emails':
            subject = "Your search didn't get any results"
            message = "Your search of {} {} {} at the domain {} didn't provide any results. If you need to contact this company, you can try the brute force search to find other people woring there.".format(self.first_name, self.middle_name, self.last_name, self.domain)
            email_from = settings.EMAIL_HOST_USER
            mail_to = 'test@gmail.com'
            send_mail(
                        subject,
                        message,
                        email_from,
                        [mail_to],
                        fail_silently=False,)

        else:
            subject = "Your search got a valid email"
            message = "Your search of {} {} {} at the domain {} got a valid email. The email is {}".format(self.first_name, self.middle_name, self.last_name, self.domain, self.valid_emails)
            email_from = settings.EMAIL_HOST_USER
            mail_to = 'test@gmail.com'
            send_mail(
                        subject,
                        message,
                        email_from,
                        [mail_to],
                        fail_silently=False,)



