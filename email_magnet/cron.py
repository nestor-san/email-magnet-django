from email_magnet.models import DetailSearch


def my_cron_job():
    """
    Created a cron job to periodically check if there are new Detailed searches
    that need to be processed. It first check the list of detail searches with
    valid email is None. Then, it launches the methods to update and save.
    Finally, it notify the user for any success or failure result.
    """
    # Retrieve the Detail Searches with valid_emails field is none
    pending_search = DetailSearch.objects.filter(valid_emails=None)
    # Loop through the retrieved Detail Searches to process
    for search in pending_search:
        # Call get_valid_email method to create list of emails and validate
        search.get_valid_email()
        # Save the updates made
        search.save()
        # Call the notify_user method to send the emails
        search.notify_user(search.user.email)
