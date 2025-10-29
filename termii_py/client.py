""" Termii API Client Module
This module provides the main client interface for interacting with the Termii API.
"""
from termii_py import config
from .exception import ClientConfigError
from .http import RequestHandler
from .services import MessageService, NumberService, SenderIDService


class TermiiClient:
    """ This client provides access to various Termii services including sender ID management, messaging, and other
    communication features.

    Args:
        api_key (str, optional): Your Termii API key. If not provided, will attempt to
            read from TERMII_API_KEY environment variable.
        base_url (str, optional): The Termii API base URL. If not provided, will attempt
            to read from TERMII_BASE_URL environment variable.

    Raises:
        TermiiConfigError: If api_key or base_url is not provided and cannot be found
            in environment variables.

    Attributes:
        api_key (str): The API key used for authentication.
        base_url (str): The base URL for API requests.

    Example:
        Using args in Termii Client (api_key & base_url):
            ``client = TermiiClient(api_key="your_api_key", base_url="your_base_url")``

        Or using environment variables (TERMII_API_KEY & TERMII_BASE_URL):
            ``client = TermiiClient()``
    """

    def __init__(self, api_key: str = None, base_url: str = None):
        self.api_key = api_key or config.TERMII_API_KEY
        self.base_url = base_url or config.TERMII_BASE_URL
        self.http = RequestHandler(self.api_key, self.base_url)
        self.sender_id = SenderIDService(self.http)
        self.message = MessageService(self.http)
        self.number = NumberService(self.http)

        if not self.api_key:
            raise ClientConfigError(
                "Missing TERMII_API_KEY. Provide via api_key parameter or TERMII_API_KEY environment variable. "
                "Get your API key at: https://app.termii.com/"
            )

        if not self.base_url:
            raise ClientConfigError(
                "Missing TERMII_BASE_URL. Provide via base_url parameter or TERMII_BASE_URL environment variable. "
                "Get your base url at: https://app.termii.com/"
            )
