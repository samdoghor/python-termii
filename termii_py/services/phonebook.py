"""
This module defines the PhonebookService class, which provides methods to interact with Termii's phonebook API
endpoints. It allows users to fetch, create, update, and delete phonebooks through the Termii API. Each method
corresponds to a specific API endpoint and handles the necessary HTTP requests and payloads.

References:
    - https://developer.termii.com/phonebook

Classes:
    PhonebookService: A service class that provides methods to manage phonebooks via Termii's API.
"""
from termii_py.http import RequestHandler


class PhonebookService:
    """
    Provides methods to manage phonebooks through Termii's API.

    The class includes methods to fetch all phonebooks, create a new phonebook, update an existing phonebook, and
    delete a phonebook. Each method constructs the appropriate API request and handles the response.

    Attributes:
        http (object): An HTTP client instance responsible for making API requests to Termii.

    """

    def __init__(self, http: RequestHandler):
        """
        Initializes the PhonebookService instance.

            Args:
                http (object): An HTTP client instance (e.g., `requests.Session`) used to perform
                    network requests to the Termii API.
        """

        self.http = http

    def fetch_phonebooks(self):
        """
            Fetches all phonebooks associated with the authenticated Termii account.
            This method sends a GET request to the `/api/phonebooks` endpoint and returns the response containing the list of phonebooks.

            Raise:
                ValueError: If the API request fails or returns an error response.

            Returns:
                A response object containing the list of phonebooks and associated metadata.

            References:
                - https://developer.termii.com/phonebook#fetch-phonebooks:~:text=phonebooks%20as%20needed.-,Fetch%20Phonebooks,-This%20endpoint%20returns

        """

        return self.http.fetch("/api/phonebooks")

    def create_phonebooks(self, phonebook_name: str, description: str = None):
        """
            Creates a new phonebook with the specified name and optional description.

            This method sends a POST request to the `/api/phonebooks` endpoint with the provided phonebook name and description in the request body.

            Args:
                phonebook_name (str): The name of the phonebook to be created. This field is required.
                description (str, optional): A brief description of the phonebook. This field is optional and can be left blank.

            Raise:
                ValueError: If the `phonebook_name` parameter is not provided or is empty. This field is required to create a phonebook.

            Returns:
                A response object containing the details of the newly created phonebook, including its unique identifier and any associated metadata.

            References:
                - https://developer.termii.com/phonebook#create--a-phonebook:~:text=12%2C%0A%20%20%22empty%22%3A%20false%0A%7D-,Create%20a%20Phonebook,-This%20endpoint%20creates
        """

        payload = {
            "phonebook_name": phonebook_name,
            "description": description,
        }

        return self.http.post("/api/phonebooks", json=payload)

    def update_phonebook(self, phonebook_id, phonebook_name: str, description: str):
        """
            Updates the details of an existing phonebook identified by its unique ID.
            This method sends a PATCH request to the `/api/phonebooks/{phonebook_id}` endpoint with the updated phonebook name and description in the request body.

            Args:
                    phonebook_id (str): The unique identifier of the phonebook to be updated. This field is required to specify which phonebook to update.
                    phonebook_name (str): The new name for the phonebook. This field is required to update the phonebook's name.
                    description (str): The new description for the phonebook. This field is required to update the phonebook's description.

            Raise:
                    ValueError: If the `phonebook_id` parameter is not provided or is empty. This field is required to
                    identify which phonebook to update. Additionally, if either the `phonebook_name` or `description`
                    parameters are not provided or are empty, a ValueError will be raised since both fields are
                    required to update the phonebook's details.

            Returns:
                    A response object containing the updated details of the phonebook, including its unique identifier, new name, new description, and any associated metadata.

            References:
                    - https://developer.termii.com/phonebook#update-phonebook:~:text=successfully%22%2C%0A%20%20%20%20%22status%22%3A%20%22success%22%0A%20%20%7D-,Update%20Phonebook,-This%20endpoint%20updates
        """

        if not phonebook_id:
            raise ValueError("phonebook_id is required to update a phonebook.")

        payload = {
            "phonebook_name": phonebook_name,
            "description": description,
        }

        return self.http.patch(f"/api/phonebooks/{phonebook_id}", json=payload)

    def delete_phonebook(self, phonebook_id):
        """
            Deletes an existing phonebook identified by its unique ID.
            This method sends a DELETE request to the `/api/phonebooks/{phonebook_id}` endpoint to remove the specified phonebook from the Termii account. Once deleted, the phonebook and all associated contacts will be permanently removed.

            Args:
                    phonebook_id (str): The unique identifier of the phonebook to be deleted. This field is required to specify which phonebook to delete.

            Raise:
                    ValueError: If the `phonebook_id` parameter is not provided or is empty. This field is required to identify which phonebook to delete.

            Returns:
                    A response object indicating the success or failure of the delete operation, including any relevant status messages or error details.

            References:
                    - https://developer.termii.com/phonebook#delete-phonebook:~:text=0%2C%0A%20%20%20%20%20%20%22numberOfCampaigns%22%3A%200%0A%20%20%7D-,Delete%20phonebook,-This%20endpoint%20deletes
        """

        if not phonebook_id:
            raise ValueError("phonebook_id is required to delete a phonebook.")

        return self.http.delete(f"/api/phonebooks/{phonebook_id}")
