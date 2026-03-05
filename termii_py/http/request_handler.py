"""
RequestHandler class for interacting with the Termii API.
Classes:
    RequestHandler
Methods:
    fetch: Sends a GET request to the Termii API.
    post: Sends a POST request to the Termii API.
"""
import requests

from .request_response import RequestResponse


class RequestHandler:
    """
    Initializes a RequestHandler instance.

    Attributes:
        api_key (str): The API key for authentication.
        base_url (str): The base URL of the Termii API.
    """

    def __init__(self, api_key, base_url):
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")

    def fetch(self, endpoint, params=None):
        """
       Sends a GET request to the Termii API.

        Args:
            endpoint (str): The endpoint to query.
            params (dict, optional): Query parameters. Defaults to None.

        Returns:
            RequestResponse: The response from the API.
        """

        params = params or {}
        params["api_key"] = self.api_key
        response = requests.get(f"{self.base_url}{endpoint}", params=params)

        return RequestResponse.handle_response(response)

    def post(self, endpoint, json: dict):
        """
        Sends a POST request to the Termii API.

        Args:
            endpoint (str): The endpoint to query.
            json (dict): The JSON payload.

        Returns:
            RequestResponse: The response from the API.
        """

        json["api_key"] = self.api_key
        response = requests.post(f"{self.base_url}{endpoint}", json=json)

        return RequestResponse.handle_response(response)

    def patch(self, endpoint, json: dict):
        """
        Sends a PATCH request to the Termii API. This method is used for updating existing resources on the Termii platform.
        The `endpoint` parameter specifies the API endpoint to which the request will be sent, while the `json`
        parameter contains the data to be updated in JSON format. The method automatically includes the API key for
        authentication in the request payload. The response from the API is processed and returned as a
        `RequestResponse` object, which encapsulates the status and data of the API response.

        Args:
            endpoint (str): The API endpoint to which the PATCH request will be sent (e.g., "/api/phonebooks/{phonebook_id}").
            json (dict): A dictionary containing the data to be updated, which will be sent as a JSON payload in the
            request body. This should include the fields that need to be updated along with their new values.

        Returns:
            RequestResponse: An object representing the response from the Termii API, which includes the status code,
            response data, and any relevant metadata. The `RequestResponse` class is responsible for handling the
            parsing and interpretation of the API response, allowing for consistent error handling and data extraction
            across different API endpoints.
        """

        json["api_key"] = self.api_key
        response = requests.patch(f"{self.base_url}{endpoint}", json=json)

        return RequestResponse.handle_response(response)

    def delete(self, endpoint, params=None):
        """
        Sends a DELETE request to the Termii API. This method is used for deleting resources from the Termii platform.
        The `endpoint` parameter specifies the API endpoint to which the request will be sent, while the `params`
        parameter contains any query parameters that need to be included in the request URL. The method automatically
        includes the API key for authentication in the query parameters. The response from the API is processed and
        returned as a `RequestResponse` object, which encapsulates the status and data of the API response.

        Args:
            endpoint (str): The API endpoint to which the DELETE request will be sent (e.g., "/api/phonebooks/{phonebook_id}").
            params (dict, optional): A dictionary of query parameters to be included in the request URL. This can include
            any additional parameters required by the API endpoint, such as filters or identifiers. If no parameters are needed, this can be left as None.

        Returns:
            RequestResponse: An object representing the response from the Termii API, which includes the status code,
            response data, and any relevant metadata. The `RequestResponse` class is responsible for handling the
            parsing and interpretation of the API response, allowing for consistent error handling and data extraction
            across different API endpoints.
        """

        params = params or {}
        params["api_key"] = self.api_key
        response = requests.delete(f"{self.base_url}{endpoint}", params=params)

        return RequestResponse.handle_response(response)

    def post_file(self, endpoint, file_path: str, data: dict):
        """
        Sends a POST request to the Termii API with a file upload. This method is used for endpoints that require file
        uploads, such as creating multiple contacts from a CSV file. The `endpoint` parameter specifies the API
        endpoint to which the request will be sent, while the `file_path` parameter specifies the local path to the
        file that needs to be uploaded. The `data` parameter contains any additional form data that needs to be
        included in the request body. The method automatically includes the API key for authentication in the form
        data. The response from the API is processed and returned as a `RequestResponse` object, which encapsulates
        the status and data of the API response.

        Args:
            endpoint (str): The API endpoint to which the POST request will be sent (e.g., "/api/contacts/upload").
            file_path (str): The local file path of the file to be uploaded (e.g., "C:/path/to/contacts.csv").
            data (dict): A dictionary containing any additional form data to be included in the request body. This can include
            fields such as "country_code" or "phonebook_id" that are required by the API endpoint.

        Returns:
            RequestResponse: An object representing the response from the Termii API, which includes the status code,
            response data, and any relevant metadata. The `RequestResponse` class is responsible for handling the
            parsing and interpretation of the API response, allowing for consistent error handling and data extraction
            across different API endpoints.
        """

        data["api_key"] = self.api_key

        files = {"file": open(file_path, "rb")}
        response = requests.post(f"{self.base_url}{endpoint}", files=files, data=data)

        return RequestResponse.handle_response(response)
