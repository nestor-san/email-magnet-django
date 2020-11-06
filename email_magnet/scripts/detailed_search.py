"""Email magnet is a simple program that, given a domain name and a personal name, is able
to guess and validate the email adress of such person. 
In order to do that, it creates list with all the possible emails schemes based on the first name,
last name, middle name and initials of those. 
When the list is crated, Email Magnet checks if the emails are valid and if they exist.
"""
import requests
from validate_email import validate_email

#Adjuts the settings for the validation request
from_adress = 'dummy@gmail.com' #You can write your adress or any valid email here
from_host = 'gmail.com' #You can use whatever host, fake or real 
smtp_timeout=10 #this is the timeout for sending smtp requests
dns_timeout=10 #this is the timout for dns

#Main method to create a list of possible emails and validate against the real server 
def detailed_search(domain, first_name=None, middle_name=None, last_name=None):
    """
    This function provides the core functionality of email magnet. It first create a list of possible emails
    with the function "email_list_generator(domain, first_name=None, middle_name=None, last_name=None)".
    Once the list is created, this function validate every email with the module "validate email". When it 
    finds a valid email, it store in a variable. 
    This function returns a list of possible emails and a list of valid emails in a tuple.
    """

    def email_list_generator(domain, first_name=None, middle_name=None, last_name=None):
        """
        This function create a list of emails based in the most common approaches companies
        use to generate their employers emails. It's based in a Rob Ousbey google doc: 
        https://docs.google.com/spreadsheets/d/17URMtNmXfEZEW9oUL_taLpGaqTDcMkA79J8TRw4xnz8/edit#gid=0
        This function returns a list of possible emails.
        """

        #Create a emails list to store possible emails
        emails = []
        
        #Get the initial of each target employer parameter if it exists
        if first_name:
            first_initial = first_name[0]
        if middle_name:
            middle_initial = middle_name[0]
        if last_name:
            last_initial = last_name[0]
        
        #Begin to populate the emails list using only the first name and the domain
        if first_name:
            emails.append('{}@{}'.format(first_name, domain))
            emails.append('{}@{}'.format(first_initial, domain))

        #Populate the emails list using only the last name and the domain
        if last_name:
            emails.append('{}@{}'.format(last_name, domain))
            emails.append('{}@{}'.format(last_initial, domain))

        #Populate the emails list using the first name, the last name and the domain    
        if (first_name and last_name):
            emails.append('{}{}@{}'.format(first_name,last_name, domain))
            emails.append('{}.{}@{}'.format(first_name,last_name, domain))
            emails.append('{}_{}@{}'.format(first_name,last_name, domain))
            emails.append('{}-{}@{}'.format(first_name,last_name, domain))
            emails.append('{}{}@{}'.format(first_initial,last_name, domain))
            emails.append('{}.{}@{}'.format(first_initial,last_name, domain))
            emails.append('{}_{}@{}'.format(first_initial,last_name, domain))
            emails.append('{}-{}@{}'.format(first_initial,last_name, domain))
            emails.append('{}{}@{}'.format(first_name,last_initial, domain))
            emails.append('{}.{}@{}'.format(first_name,last_initial, domain))
            emails.append('{}_{}@{}'.format(first_name,last_initial, domain))
            emails.append('{}-{}@{}'.format(first_name,last_initial, domain))
            emails.append('{}{}@{}'.format(first_initial,last_initial, domain))
            emails.append('{}.{}@{}'.format(first_initial,last_initial, domain))
            emails.append('{}_{}@{}'.format(first_initial,last_initial, domain))
            emails.append('{}-{}@{}'.format(first_initial,last_initial, domain))
            #Same but backwards
            emails.append('{}{}@{}'.format(last_name, first_name,domain))
            emails.append('{}.{}@{}'.format(last_name, first_name,domain))
            emails.append('{}_{}@{}'.format(last_name, first_name,domain))
            emails.append('{}-{}@{}'.format(last_name, first_name,domain))
            emails.append('{}{}@{}'.format(last_name,first_initial, domain))
            emails.append('{}.{}@{}'.format(last_name, first_initial, domain))
            emails.append('{}_{}@{}'.format(last_name, first_initial, domain))
            emails.append('{}-{}@{}'.format(last_name, first_initial, domain))
            emails.append('{}{}@{}'.format(last_initial, first_name, domain))
            emails.append('{}.{}@{}'.format(last_initial, first_name, domain))
            emails.append('{}_{}@{}'.format(last_initial, first_name, domain))
            emails.append('{}-{}@{}'.format(last_initial, first_name, domain))
            emails.append('{}{}@{}'.format(last_initial, first_initial, domain))
            emails.append('{}.{}@{}'.format(last_initial, first_initial, domain))  
            emails.append('{}_{}@{}'.format(last_initial, first_initial, domain))  
            emails.append('{}-{}@{}'.format(last_initial, first_initial, domain))

        #Populate the emails list if middle name is provided
        if (first_name and middle_name and last_name):
            emails.append('{}{}{}@{}'.format(first_initial, middle_initial,last_name, domain))
            emails.append('{}.{}.{}@{}'.format(first_initial, middle_initial,last_name, domain))
            emails.append('{}_{}_{}@{}'.format(first_initial, middle_initial,last_name, domain))
            emails.append('{}-{}-{}@{}'.format(first_initial, middle_initial,last_name, domain))
            emails.append('{}{}.{}@{}'.format(first_initial, middle_initial,last_name, domain))
            emails.append('{}{}_{}@{}'.format(first_initial, middle_initial,last_name, domain))
            emails.append('{}{}-{}@{}'.format(first_initial, middle_initial,last_name, domain))
            emails.append('{}{}{}@{}'.format(first_name, middle_initial,last_name, domain))
            emails.append('{}.{}.{}@{}'.format(first_name, middle_initial,last_name, domain))
            emails.append('{}_{}_{}@{}'.format(first_name, middle_initial,last_name, domain))
            emails.append('{}-{}-{}@{}'.format(first_name, middle_initial,last_name, domain))
            emails.append('{}{}{}@{}'.format(first_name, middle_name,last_name, domain))
            emails.append('{}.{}.{}@{}'.format(first_name, middle_name,last_name, domain))
            emails.append('{}_{}_{}@{}'.format(first_name, middle_name,last_name, domain))
            emails.append('{}-{}-{}@{}'.format(first_name, middle_name,last_name, domain))

        #Lowercase the emails list
        emails = [element.lower() for element in emails]
        #Print the list of generated emails
        print("""
    ---------------------------------------------------------
    The following list of emails have been generated
    ---------------------------------------------------------
        """)
        print(emails)
        #Return the email list
        return emails

    #Call the function email_list_generator and store in the variable "emails"
    #Emails will hold the list of generated emails
    emails = email_list_generator(domain, first_name, middle_name, last_name)

    #Create a list to append validated emails
    valid_emails = []

    #Loop through the list of generated emails 
    for email in emails:
        #Check if an email adress is valid. Store the value in "is_valid"
        is_valid = validate_email(email_address=email, check_regex=True, check_mx=True, from_address=from_adress, helo_host=from_host, smtp_timeout=smtp_timeout, dns_timeout=dns_timeout, use_blacklist=False, debug=False)
        #If "is_valid" is True, it means the email is validated.
        if (is_valid==True):
            #Append the email to the valid emails list
            valid_emails.append(email)
            #Print the good news to the terminal
            print("""
------------------------------------------
We found a valid email with your search query
            """)
            print('One email you\'re looking for is {}'.format(email))
            print('------------------------------------------')

    #Give some feedback if there are no valid emails
    if not valid_emails:
        valid_emails.append('There are no valid emails')
    
    #Convert the valid emails list to a readable string
    separator = ', '
    valid_emails = separator.join(valid_emails)    

    #Return the list of possible emails and the list of validated emails (or the message 'There are no valid emails' if failed to validate any domain)
    return emails, valid_emails

"""
You can test the function if necessary. Uncomment the last line.
After testing, leave it commented.
"""
#detailed_search('xemob.com', 'nestor', None, None)