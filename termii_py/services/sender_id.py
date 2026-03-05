"""
SenderIDService class for managing sender IDs.
Classes:
    SenderIDService
Methods:
    fetch_id: Retrieves a list of sender IDs based on query parameters.
    request_id: Requests a new sender ID.
"""
from termii_py.http import RequestHandler


class SenderIDService:
    """
    Provides methods for interacting with sender IDs.

    Attributes:
        http: An instance of the HTTP client.

    References:
        https://developer.termii.com/sender-id
    """

    def __init__(self, http: RequestHandler):
        """
        Initializes a SenderIDService instance.

        Args:
            http: An instance of the HTTP client.
        """

        self.http = http

    def fetch_id(self, name: str = None, status: str = None):
        """
        Retrieves a list of sender IDs based on query parameters.

        Args:
            name (str, optional): The name of the sender ID. Defaults to None.
            status (str, optional): The status of the sender ID. Defaults to None.

        Returns:
            The response from the API.

        References:
            https://developer.termii.com/sender-id#:~:text=request%20methods%2C%20respectively.-,Fetch%20Sender%20ID,-The%20Fetch%20Sender
        """

        params = {}
        if name:
            params["name"] = name

        if status:
            params["status"] = status

        return self.http.fetch("/api/sender-id", params=params)

    def request_id(self, sender_id: str, usecase: str, company: str):
        """
        Requests a new sender ID.

        Args:
            sender_id (str): The desired sender ID.
            usecase (str): The use case for the sender ID.
            company (str): The company name.

        References:
            https://developer.termii.com/sender-id#:~:text=5%2C%0A%20%20%20%20%22empty%22%3A%20false%0A%7D-,Request%20Sender%20ID,-The%20Request%20Sender
        Returns:
            The response from the API.
        """

        payload = {
            "sender_id": sender_id,
            "usecase": usecase,
            "company": company
        }

        return self.http.post("/api/sender-id/request", json=payload)
