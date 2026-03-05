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

        """

        json["api_key"] = self.api_key
        response = requests.patch(f"{self.base_url}{endpoint}", json=json)

        return RequestResponse.handle_response(response)

    def delete(self, endpoint, params=None):
        """

        """

        params = params or {}
        params["api_key"] = self.api_key
        response = requests.delete(f"{self.base_url}{endpoint}", params=params)

        return RequestResponse.handle_response(response)

    def post_file(self, endpoint, file_path: str, data: dict):
        """

        """

        data["api_key"] = self.api_key

        files = {"file": open(file_path, "rb")}
        response = requests.post(f"{self.base_url}{endpoint}", files=files, data=data)

        return RequestResponse.handle_response(response)
