"""
This module contains the HTTP request handler and response classes for the Termii Python SDK. The RequestHandler class
is responsible for making HTTP requests to the Termii API, while the RequestResponse class encapsulates the response
received from the API, including status code, headers, and body content.
"""

from .request_handler import RequestHandler
from .request_response import RequestResponse
