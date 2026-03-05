"""
This module defines the `MessageService` class, which provides an interface for sending messages
through Termii's Messaging API.

It supports sending single SMS messages, WhatsApp messages, and bulk messages while ensuring
parameter validation and correct channel-type combinations before making HTTP requests to the API.

References:
    - https://developer.termii.com/messaging-api

Classes:
    MessageService: Handles message dispatch operations via Termii's Messaging API.
"""

from hmac import compare_digest

from termii_py.http import RequestHandler
from termii_py.value_object import PhoneNumber


class MessageService:
    """
    Provides methods for sending SMS, WhatsApp, and bulk messages via Termii's Messaging API.

    The class ensures data validation and enforces correct message channel and type usage.
    Each method constructs the appropriate request payload and sends it using the injected
    HTTP client.

    Attributes:
        http (object): An HTTP client instance responsible for making API requests.
    """

    def __init__(self, http: RequestHandler):
        """
        Initializes the MessageService instance.

        Args:
            http (object): An HTTP client instance (e.g., `requests.Session`) used to perform
                network requests to the Termii API.
        """

        self.http = http

    def send_message(self, sent_to: str, sent_from: str, message: str, channel: str, type: str):
        """
        Sends a single SMS message through Termii's Messaging API.

        This method supports the following channels:
        - "generic" (for standard messaging)
        - "dnd" (for messages that bypass Do-Not-Disturb filters)
        - "voice" (for voice call messages)

        Notes:
            - WhatsApp messages must be sent using `send_whatsapp_message()`.
            - For voice messages, the `type` parameter must explicitly be set to "voice".

        Args:
            sent_to (str): Recipient’s phone number in international format.
            sent_from (str): The sender ID registered on Termii.
            message (str): The content of the message to be sent.
            channel (str): The communication channel. Must be one of ["generic", "dnd", "voice"].
            type (str): The message type (e.g., "plain", "voice").

        Raises:
            ValueError: If an invalid channel-type combination is provided.
            ValueError: If attempting to send WhatsApp messages via this method.
            ValueError: If `channel` or `type` parameters are invalid.

        Returns:
            dict: The JSON response returned by the Termii API.

        References:
            https://developer.termii.com/messaging-api#:~:text=Send%20message
        """

        PhoneNumber(sent_to)

        if compare_digest("whatsapp", str(channel).strip().lower()):
            raise ValueError("For WhatsApp messages, please use the 'send_whatsapp_message' method.")

        if compare_digest("voice", str(channel).strip().lower()) and not compare_digest("voice",
                                                                                        str(type).strip().lower()):
            raise ValueError("For voice channel, the 'type' parameter must be set to 'voice'.")

        if not compare_digest("generic", str(channel).strip().lower()) and not compare_digest("dnd",
                                                                                              str(channel).strip().lower() or not compare_digest(
                                                                                                  "voice",
                                                                                                  str(channel).strip().lower())):
            raise ValueError("The 'channel' parameter must be either 'generic' or 'dnd' or voice.")

        payload = {
            "to": sent_to,
            "from": sent_from,
            "sms": message,
            "channel": channel,
            "type": type
        }

        return self.http.post("/api/sms/send", json=payload)

    def send_whatsapp_message(self, sent_to: str, sent_from: str, message: str, url: str = None, caption: str = None):
        """
       Sends a WhatsApp message through Termii's Messaging API.

        This endpoint supports text-only and media messages (e.g., image or document links).

        Args:
            sent_to (str): Recipient’s phone number in international format.
            sent_from (str): The sender ID or WhatsApp business number.
            message (str): Text message to be sent.
            url (str, optional): Media URL for attachments (image, document, etc.).
            caption (str, optional): Caption for the media file (if applicable).

        Raises:
            ValueError: If the recipient phone number is invalid.

        Returns:
            dict: The JSON response from the Termii API.

        References:
            https://developer.termii.com/messaging-api#:~:text=Send%20WhatsApp%20Message%20(Conversational)
       """

        PhoneNumber(sent_to)

        payload = {
            "to": sent_to,
            "from": sent_from,
            "sms": message,
            "channel": "whatsapp",
            "type": "plain",
            "media": {
                "url": url,
                "caption": caption,
            }
        }

        return self.http.post("/api/sms/send", json=payload)

    def send_bulk_message(self, sent_to: list, sent_from: str, message: str, channel: str, type: str):
        """
        Sends bulk SMS messages to multiple recipients using Termii's Messaging API.

        This method supports sending to multiple phone numbers in one request. Only the "generic"
        and "dnd" channels are supported for bulk operations.

        Notes:
            - Voice and WhatsApp messages cannot be sent in bulk.
            - Each recipient number is validated before sending.

        Args:
            sent_to (list): A list of recipient phone numbers in international format.
            sent_from (str): The sender ID registered on Termii.
            message (str): The content of the message to be sent.
            channel (str): The message channel. Must be either "generic" or "dnd".
            type (str): The message type (e.g., "plain").

        Raises:
            ValueError: If any recipient number is invalid.
            ValueError: If attempting to send WhatsApp or voice messages in bulk.
            ValueError: If an invalid channel is specified.

        Returns:
            dict: The JSON response returned by the Termii API.

        References:
            https://developer.termii.com/messaging-api#:~:text=Send%20Bulk%20message
        """

        for x in sent_to:
            PhoneNumber(x)

        if compare_digest("whatsapp", str(channel).strip().lower()):
            raise ValueError("For WhatsApp messages, please use the 'send_whatsapp_message' method.")

        if compare_digest("voice", str(channel).strip().lower()) or compare_digest("voice", str(type).strip().lower()):
            raise ValueError("Voice messages are not supported in bulk messaging.")

        if not compare_digest("generic", str(channel).strip().lower()) and not compare_digest("dnd",
                                                                                              str(channel).strip().lower()):
            raise ValueError("The 'channel' parameter must be either 'generic' or 'dnd' or voice.")

        payload = {
            "to": sent_to,
            "from": sent_from,
            "sms": message,
            "channel": channel,
            "type": type
        }

        return self.http.post("/api/sms/send/bulk", json=payload)
