"""
This module provides a client for interacting with the Termii API, which allows you to send SMS messages, manage
contacts, and perform other communication-related tasks. The TermiiClient class encapsulates the functionality needed
to make API requests and handle responses effectively.
"""

from .client import TermiiClient

__all__ = ["TermiiClient"]
__version__ = "0.1.0"
