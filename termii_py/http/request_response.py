"""
RequestResponse class for handling API responses.
Classes:
    RequestResponse
Methods:
    handle_response: Processes an HTTP response and returns a RequestResponse instance.
"""
from hmac import compare_digest


class RequestResponse:
    """
    Represents a standardized API response.

    Attributes:
        status_code (int): The HTTP status code of the response.
        status (str): A string indicating the status of the response (e.g., "ok" or "error").
        message (str | dict): The response message, which can be a string or a dictionary.
    """

    def __init__(self, status_code: int, status, message: str | dict):
        """
        Initializes a RequestResponse instance.

        Args:
            status_code (int): The HTTP status code of the response.
            status (str): A string indicating the status of the response.
            message (str | dict): The response message.
        """
        self.status_code = status_code
        self.status = status
        self.message = message

    @staticmethod
    def handle_response(response):
        """
        Processes an HTTP response and returns a RequestResponse instance.

        Args:
            response: The HTTP response object.

        Returns:
            RequestResponse: An instance representing the API response.

        Notes:
            This method checks the HTTP status code of the response and returns a RequestResponse instance with a
            standardized status and message.
        """

        if compare_digest(str(response.status_code), "200") or compare_digest(str(response.status_code), "201"):
            return RequestResponse(
                status_code=response.status_code,
                status="ok",
                message=response.text
            )

        if not compare_digest(str(response.status_code), "200"):
            return RequestResponse(
                status_code=response.status_code,
                status="error",
                message=response.text
            )

        return None
