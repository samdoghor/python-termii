"""
This module provides the ContactService class, which allows you to manage contacts within a phonebook. You can fetch
existing contacts, create new contacts (individually or in bulk), and delete contacts from a specified phonebook.
The service interacts with the Termii API to perform these operations.

References:
    - https://developer.termii.com/contacts

Classes:
    ContactService: A service class that provides methods to manage contacts within a phonebook via Termii's API.
"""
from termii_py.http import RequestHandler


class ContactService:
    """
    Provides methods to manage contacts within a phonebook through Termii's API.
    The class includes methods to fetch contacts, create new contacts (individually or in bulk), and delete contacts from a specified phonebook. Each method constructs the appropriate API request and handles the response.

    Attributes:
        http (object): An HTTP client instance responsible for making API requests to Termii.
    """

    def __init__(self, http: RequestHandler):
        """
        Initializes the ContactService instance.

        Args:
            http (object): An HTTP client instance (e.g., `requests.Session`) used to perform network requests to the Termii API.
        """

        self.http = http

    def fetch_contacts(self, phonebook_id: str):
        """
            Fetches all contacts associated with a specific phonebook. This method sends a GET request to
            the `/api/phonebooks/{phonebook_id}/contacts` endpoint, where `{phonebook_id}` is the unique identifier of
            the phonebook whose contacts you want to retrieve. The response will contain a list of contacts along with
            their details.

            Args:
                phonebook_id (str): The unique identifier of the phonebook for which to fetch contacts.

            Raises:
                ValueError: If the `phonebook_id` is not provided or is invalid.

            Returns:
                A response object containing the list of contacts and associated metadata for the specified phonebook.

            References:
                - https://developer.termii.com/contacts#:~:text=within%20your%20phonebooks.-,Fetch%20contacts%20by%20phonebook%20ID,-This%20endpoint%20retrieves
        """

        if not phonebook_id:
            raise ValueError("phonebook_id is required")

        return self.http.fetch(f"/api/phonebooks/{phonebook_id}/contacts")

    def create_contact(self, phonebook_id, phone_number: str, country_code: str, email_address: str = None,
                       first_name: str = None, last_name: str = None, company: str = None):
        """
            Creates a new contact within a specified phonebook. This method sends a POST request to
            the `/api/phonebooks/{phonebook_id}/contacts` endpoint, where `{phonebook_id}` is the unique identifier of
            the phonebook to which the contact will be added. The request body should include the contact's
            phone number, country code, and optionally their email address, first name, last name, and company. The
            response will contain the details of the newly created contact.

            Args:
                phonebook_id (str): The unique identifier of the phonebook to which the contact will be added.
                phone_number (str): The contact's phone number (without the country code).
                country_code (str): The country code for the contact's phone number (without the '+' sign).
                email_address (str, optional): The contact's email address. This field is optional.
                first_name (str, optional): The contact's first name. This field is optional.
                last_name (str, optional): The contact's last name. This field is optional.
                company (str, optional): The contact's company name. This field is optional.

            Raises:
                ValueError: If the `phonebook_id` is not provided or is invalid.
                ValueError: If the `country_code` starts with a '+' sign. The country code should be provided without the '+' sign.

            Returns:
                A response object containing the details of the newly created contact, including its unique identifier and any associated metadata.

            References:
                - https://developer.termii.com/contacts#add-single-contacts-to-phonebook:~:text=12%2C%0A%20%20%20%20%22empty%22%3A%20false%0A%20%20%7D%0A%7D-,Add%20single%20contacts%20to%20phonebook,-This%20endpoint%20allows
        """

        if not phonebook_id:
            raise ValueError("phonebook_id is required")

        if country_code.startswith("+"):
            raise ValueError("country code should not start with '+' sign.")

        payload = {
            "phone_number": phone_number,
            "country_code": country_code,
            "email_address": email_address,
            "first_name": first_name,
            "last_name": last_name,
            "company": company,
        }

        return self.http.post(f"/api/phonebooks/{phonebook_id}/contacts", json=payload)

    def create_multiple_contacts(self, phonebook_id, country_code: str, file_path: str, ):
        """
            Creates multiple contacts in bulk by uploading a CSV file containing the contact details. This method sends
            a POST request to the `/api/phonebooks/contacts/upload` endpoint with the specified phonebook ID, country
            code, and file path. The CSV file should be formatted according to Termii's requirements, with columns for
            phone number, email address, first name, last name, and company. The response will indicate the success or
            failure of the bulk upload operation.

            Args:
                phonebook_id (str): The unique identifier of the phonebook to which the contacts will be added.
                country_code (str): The country code for the contacts' phone numbers (without the '+' sign).
                file_path (str): The file path to the CSV file containing the contact details to be uploaded.

            Raises:
                ValueError: If the `phonebook_id` is not provided or is invalid.
                ValueError: If the `country_code` starts with a '+' sign. The country code should be provided without the '+' sign.
                ValueError: If the `file_path` is not provided or is invalid. The file path must point to a valid CSV file containing the contact details.

            Returns:
                A response object indicating the success or failure of the bulk contact upload operation, along with any relevant metadata or error messages.

            References:
                - https://developer.termii.com/contacts#add-single-contacts-to-phonebook:~:text=Promise%22%2C%0A%20%20%20%20%22last_name%22%3A%20%22John%22%0A%20%20%7D%0A%7D-,Add%20multiple%20contacts%20to%20phonebook,-This%20endpoint%20allows
        """

        if not phonebook_id:
            raise ValueError("phonebook_id is required")

        if country_code.startswith("+"):
            raise ValueError("country code should not start with '+' sign.")

        data = {
            "phonebook_id": phonebook_id,
            "country_code": country_code,
        }

        return self.http.post_file(f"/api/phonebooks/contacts/upload", data=data, file_path=file_path)

    def delete_contact(self, phonebook_id):
        """
            Deletes all contacts associated with a specific phonebook. This method sends a DELETE request to the
            `/api/phonebooks/{phonebook_id}/contacts` endpoint, where `{phonebook_id}` is the unique identifier of the
            phonebook from which to delete contacts. The response will indicate the success or failure of the delete
            operation. Note that this action will remove all contacts from the specified phonebook, so use it with
            caution.

            Args:
                phonebook_id (str): The unique identifier of the phonebook from which to delete contacts.

            Raises:
                ValueError: If the `phonebook_id` is not provided or is invalid. The `phonebook_id` is required to identify which phonebook's contacts should be deleted.

            Returns:
                A response object indicating the success or failure of the delete operation, along with any relevant metadata or error messages. The response may include information about the number of contacts deleted or any issues encountered during the process.

            References:
                - https://developer.termii.com/contacts#add-single-contacts-to-phonebook:~:text=get%20it%20done.%22%0A%20%20%7D-,Delete%20Contact%20in%20a%20Phonebook,-This%20endpoint%20allows
        """

        if not phonebook_id:
            raise ValueError("phonebook_id is required to delete contacts.")

        return self.http.delete(f"/api/phonebooks/{phonebook_id}/contacts")
