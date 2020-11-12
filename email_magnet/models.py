from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from email_magnet.scripts import detailed_search
from django.core.mail import send_mail
import requests


def name_help_text(type):
    return f"""The {type} name of employer at the company that you're
           targetting. It is recommended to fill in this field"""


class DetailSearch(models.Model):
    """
    This model create a DetailSearch instance. This is the basic unit of email
    magnet Detail Search Tool. In this class, the user provides the data which
    allow the system to create a list of possible emails and validate against
    the email server of the user.  This way, it can provide a list of
    validated emails ready to be used.
    """
    # The domain name of the targeted company
    domain = models.CharField(
        max_length=40, verbose_name="Domain name",
        help_text="""The domain name of the company that you're targetting.
                  *This is a required field.""")
    # The first name of the targeted employer
    first_name = models.CharField(max_length=30,
                                  blank=True,
                                  verbose_name="First name",
                                  help_text=name_help_text('first'))
    # The middle name of the targeted employer
    middle_name = models.CharField(max_length=30,
                                   blank=True,
                                   verbose_name="Middle name",
                                   help_text=name_help_text('middle'))
    # The last name of the targeted employer
    last_name = models.CharField(max_length=30,
                                 blank=True,
                                 verbose_name="Last name",
                                 help_text=name_help_text('last'))
    # Foreign key of user, who owns the DetailSearch instance
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # A list of possible emails, which can be null until is processed
    possible_emails = models.TextField(null=True)
    # A list of validated emails, which can be null until is processed
    valid_emails = models.TextField(null=True)

    def __str__(self):
        """
        String function provides the relevant search information in a friendly
        way.  Such as "Search for Nestor Sanchez at nestorsan.com".
        If you do, say "Hello!".
        """
        name = 'Search for {} {} {} at {}'.format(self.first_name,
                                                  self.middle_name,
                                                  self.last_name,
                                                  self.domain)
        return name

    def get_valid_email(self):
        """
        This method checks if it's possible to find a valid email with the
        details provided(domain & first/middle/last name). It loads the
        function from "detailed_search.py" at scripts folder.
        This method is called periodically by a cron job ("cron.py" at main
        folder). Settings of the cron job can be located at "settings.py".
        Note you should remove previous cron job and create a new one if you
        make any changes in the cron at settings.py.
        This function is not saving the instance. The instance.save() is
        called from the cron job. But you can call self.save() to save from
        here if you need to modify the behaviour of the tool.
        """
        # Create a variable to store the results of the search.
        # Results come in a list of two elements.
        emails = detailed_search.detailed_search(self.domain,
                                                 self.first_name,
                                                 self.middle_name,
                                                 self.last_name)
        self.possible_emails = emails[0]  # load the possible emails list
        self.valid_emails = emails[1]  # load the valid emails list

    def notify_user(self, user_email):
        """
        This method sends an email to the user with the results, whether
        there are valid emails found or not. This method is called from the
        cron job ("cron.py" at main folder). Settings of the cron job can be
        located at "settings.py". Note you should remove previous cron job
        and create a new one if you make any changes in the cron at
        settings.py.
        """
        # Check the contents of valid emails field. If ther result is
        # 'There are no valid emails' it means the system  wasnt' able to find
        # a valid email with the details provided by the user.
        if self.valid_emails == 'There are no valid emails':
            # Create subject of the email
            subject = "Your search didn't get any results"
            # Create message of the email
            message = """Your search of {} {} {} at the domain {} didn't
                      provide any results. If you need to contact this
                      company, you can try the brute force search to find
                      other people woring there.""".format(self.first_name,
                                                           self.middle_name,
                                                           self.last_name,
                                                           self.domain)
            # Get email from info from settings
            email_from = settings.EMAIL_HOST_USER
            # Get email to info from the user who owns the serach.
            mail_to = user_email
            # Launch send_mail function provided by default by Django
            send_mail(
                        subject,
                        message,
                        email_from,
                        [mail_to],
                        fail_silently=False,)

        # The following code launches if there are valid emails
        else:
            # Create subject of the email
            subject = "Your search got a valid email"
            # Create message of the email and include the valid email result
            message = """Your search of {} {} {} at the domain {} got a valid
                      email. The email is {}""".format(self.first_name,
                                                       self.middle_name,
                                                       self.last_name,
                                                       self.domain,
                                                       self.valid_emails)
            # Get email from info from settings
            email_from = settings.EMAIL_HOST_USER
            # Get email to info from the user who owns the serach.
            mail_to = user_email
            # Launch send_mail function provided by default by Django Framework
            # with the data loaded above
            send_mail(
                        subject,
                        message,
                        email_from,
                        [mail_to],
                        fail_silently=False,)


class BruteForceSearch(models.Model):
    """
    This model creates a BruteForceSearch instance. A BruteForceSearch means a
    search where only the domain name is provided. This way, the system must
    perform several actions to try to find valid email adresses at this company
    domain. First of all, it checks common emails names such as info, finance,
    admin, etc... Then, it search online for public emails at the domain name
    given and employers names. In case it find employers names, it try the
    detail search function with them to validate email names. Finally, it
    validates all the possible emails and store them.

    ---------------------------------------------------------------------------------------------------

        BRUTE FOR SEARCH IS UNDER DEVELOPMENT

        BRUTE FOR SEARCH IS NOT AVAILABLE YET

        SORRY FOR THE INCONVENIENCE

    ---------------------------------------------------------------------------------------------------
    """
    # Domain name of the targeted company, provided by the user
    domain = models.CharField(max_length=40,
                              verbose_name="Domain name",
                              help_text="""The domain name of the company that
                              you're targetting. *This is a required field.""")
    # List of possible emails, is null at instantiation
    possible_emails = models.TextField(null=True)
    # List of employers names, is null at instantiation
    employers_names = models.TextField(null=True)

    def __str__(self):
        """
        String function provides the relevant search information in a
        friendly way. Such as "Brute for search nestorsan.com". If you
        get any success, please, say "Hello!".
        """
        name = 'Brute for search for {}.'.format(self.domain)
        return name

    def get_auto_emails(self):
        """
        It creates a list with the most common emails that business use such as
        info@domain.com and similar ones and return the list.
        """
        # Create an empty list to append automatic generated emails
        emails = []
        # List with the most common corporative emails adresses.
        # Feel free to add or remove any item.
        auto_adress = ['info', 'accounts', 'finance', 'admin', 'support',
                       'billing', 'hello', 'careers', 'domains', 'partners',
                       'press', 'hi', 'hey', 'howdy', 'yourfriends', 'sales',
                       'marketing', 'noreply', 'bounces', 'design',
                       'operation', 'operations', 'bookings', 'orders',
                       'customer', 'customers']
        # For loop through the common corporative email adresses
        for adress in auto_adress:
            # Convert the corp string to a valid email of the target domain
            email = adress + '@' + self.domain
            # Append the valid email to the emails list.
            # For example, info@nestorsan.com or accounts@nestorsan.com
            emails.append(email)
        # Return the list of possible emails
        return emails

    def search_for_emails(self):
        """
        Search for emails that have been publically exposed on internet.
        Function is BEING DEVELOPED.

        ---------------------------------------------------------------------------------------------------

        BRUTE FOR SEARCH IS NOT AVAILABLE YET

        ---------------------------------------------------------------------------------------------------
        """
        string_search = '@' + self.domain
        # emails = []
        url = "https://rapidapi.p.rapidapi.com/api/Search/WebSearchAPI"

        querystring = {"pageNumber": "1", "q": string_search,
                       "autoCorrect": "true", "pageSize": "10"}

        headers = {
            'x-rapidapi-key': "",
            'x-rapidapi-host':
                "contextualwebsearch-websearch-v1.p.rapidapi.com"
            }

        response = requests.request("GET", url, headers=headers,
                                    params=querystring)

        print(response)

        return response
