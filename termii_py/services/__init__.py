"""
This module contains the service classes for interacting with the Termii API. Each service class corresponds to a
specific aspect of the Termii platform, such as managing campaigns, contacts, messages, numbers, phonebooks, sender IDs,
and templates. These classes provide methods to perform various operations related to their respective domains,
allowing users to easily integrate Termii's functionality into their applications.
"""

from .campaign import CampaignService
from .contact import ContactService
from .message import MessageService
from .number import NumberService
from .phonebook import PhonebookService
from .sender_id import SenderIDService
from .template import TemplateService
