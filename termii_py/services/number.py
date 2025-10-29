"""
This module defines the `NumberService` class, which provides functionality for sending messages
directly to a phone number through Termii's Number Messaging API.

The service validates the recipient’s phone number format before dispatching messages
and uses the provided `RequestHandler` instance to make HTTP requests to the Termii API.

References:
    - https://developer.termii.com/number
"""

from termii_py.http import RequestHandler
from termii_py.value_object import PhoneNumber


class NumberService:
    """
    Provides functionality for sending messages to individual phone numbers
    using Termii’s Number Messaging API endpoint.

    This class ensures that phone numbers are properly validated before
    sending and abstracts the HTTP request handling via the injected `RequestHandler`.

    Attributes:
        http (RequestHandler): The HTTP request handler instance used to communicate
            with Termii’s API endpoints.

    References:
        - https://developer.termii.com/number#:~:text=Join%20Loop-,Number%20API,-This%20API%20allows
    """

    def __init__(self, http: RequestHandler):
        """
     Initializes the `NumberService` with an HTTP client for API communication.

        Args:
            http (RequestHandler): The request handler responsible for making
                authenticated HTTP requests to Termii’s API.

        References:
            - https://developer.termii.com/number#:~:text=Join%20Loop-,Number%20API,-This%20API%20allows
        """

        self.http = http

    def send_message(self, sent_to: str, message: str):
        """
        Sends an SMS message directly to a specific phone number using Termii’s
        Number Messaging API endpoint.

        This method validates the provided phone number using the `PhoneNumber`
        value object before constructing the payload and dispatching the message.

        Args:
            sent_to (str): The recipient’s phone number in international format (e.g., "2348012345678").
            message (str): The text message to send.

        Raises:
            ValueError: If the provided phone number is invalid.

        Returns:
            dict: The JSON response returned by the Termii API.

        References:
            - https://developer.termii.com/number#:~:text=to%20customers%20location.-,Send%20Message,-Endpoint%20%3A%20https
        """

        PhoneNumber(sent_to)

        payload = {
            "to": sent_to,
            "sms": message,
        }

        return self.http.post("/api/sms/number/send", json=payload)
