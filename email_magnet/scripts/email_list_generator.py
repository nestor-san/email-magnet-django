"""
This function create a list of emails based in the most common approaches companies
use to generate their employers emails. It's based in a Rob Ousbey google doc: 
https://docs.google.com/spreadsheets/d/17URMtNmXfEZEW9oUL_taLpGaqTDcMkA79J8TRw4xnz8/edit#gid=0
This function returns a list of possible emails.
"""
def email_list_generator(domain, first_name=None, middle_name=None, last_name=None):
    #Create a emails list to store emails
    emails = []
    
    #Get the initial of each parameter if it exist
    if first_name:
        first_initial = first_name[0]
    if middle_name:
        middle_initial = middle_name[0]
    if last_name:
        last_initial = last_name[0]
    
    #Begin to populate the emails list using only the first name and the domain
    if first_name:
        emails.append('{}@{}'.format(first_name, domain))

    #Populate the emails list using only the last name and the domain
    if last_name:
        emails.append('{}@{}'.format(last_name, domain))

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
