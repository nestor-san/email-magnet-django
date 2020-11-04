"""Email magnet is a simple program that, given a domain name and a personal name, is able
to guess and validate the email adress of such person. 
In order to do that, it creates list with all the possible emails schemes based on the first name,
last name, middle name and initials of those. 
When the list is crated, Email Magnet checks if the emails are valid and if they exist.
"""
import requests
from email_list_generator import email_list_generator
from validate_email import validate_email

#Adjuts the settings for the validation request
from_adress = 'dummy@gmail.com'
from_host = 'gmail.com'
smtp_timeout=10
dns_timeout=10

#Main method to create a list of possible emails and validate against the real server 
def detailded_search(domain, first_name=None, middle_name=None, last_name=None):
    emails = email_list_generator(domain, first_name, middle_name, last_name)
    for email in emails:
        is_valid = validate_email(email_address=email, check_regex=True, check_mx=True, from_address=from_adress, helo_host=from_host, smtp_timeout=smtp_timeout, dns_timeout=dns_timeout, use_blacklist=False, debug=False)
        if (is_valid==True):
            print("""
------------------------------------------
We found a valid email with your search query
            """)
            print('The email you\'re looking for is {}'.format(email))
            print('------------------------------------------')
            return email
"""
Test the function if necessary
"""
#detailded_search('xemob.com', 'nestor', None, 'Sanchez')