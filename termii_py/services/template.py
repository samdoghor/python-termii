"""
This module defines the `TemplateService` class, which provides functionality for sending messages
using predefined templates via Termii's Template Messaging API.

The service validates the recipient’s phone number format before dispatching messages
and uses the provided HTTP client instance to make requests to the Termii API.

References:
    - https://developer.termii.com/templates

Classes:
    TemplateService: Handles message dispatch operations via Termii's Template Messaging API.
"""
from termii_py.value_object import PhoneNumber


class TemplateService:
    """
    Provides methods for sending messages using predefined templates via Termii's Template Messaging API.

    The class ensures data validation before making HTTP requests to the API. Each method constructs the appropriate
    request payload and sends it using the injected HTTP client.

    Attributes:
        http: An instance of the HTTP client.
    """

    def __init__(self, http):
        """
        Initializes a SenderIDService instance.

        Args:
            http: An instance of the HTTP client.
        """

        self.http = http

    def send_message(self, sent_to: str, device_id: str, template_id: str, data: dict, caption: str = None,
                     url: str = None):
        """

        Sends a message using a predefined template via Termii's Template Messaging API.

        Args:
            sent_to (str): The recipient’s phone number in international format. e.g., "2348012345678".
            device_id (str): The device ID associated with the template.
                                (Represents the Device ID for Whatsapp. It can be Alphanumeric. It should be passed
                                when the message is sent via whatsapp (It can be found on the manage device page on
                                your Termii dashboard))
            template_id (str): The ID of the message template to use.
            data (dict): A dictionary containing placeholder values to populate the template.
                        Represents the variables used in your WhatsApp template. These key-value pairs will dynamically
                        populate the placeholders in your approved template message. You can find the required keys for
                         each template on the Device Subscription page of your dashboard.
                        (Example: {"studname": "Victor", "average": "30" })
            caption (str, optional): The caption for the media (if sending media). Defaults to None.
            url (str, optional): The URL of the media to send (if sending media). Defaults to None.

        Raises:
            ValueError: If the provided phone number is invalid.

        Returns:
            dict: The JSON response returned by the Termii API.

        References:
            https://developer.termii.com/templates

        """

        if caption is not None and url is None:
            raise ValueError("If caption is provided, url must also be provided to send media.")

        if caption is None and url is not None:
            raise ValueError("If url is provided, caption must also be provided to send media.")

        endpoint = "/api/send/template"

        PhoneNumber(sent_to)

        if not isinstance(data, dict):
            raise ValueError("The 'data' parameter must be a dictionary containing template placeholder values.")

        payload = {
            "phone_number": sent_to,
            "device_id": device_id,
            "template_id": template_id,
            "data": data,
        }

        if caption is not None and url is not None:
            endpoint = "/api/send/template/media"

            payload['media'] = {
                "caption": caption,
                "url": url
            }

        return self.http.post(endpoint, json=payload)
