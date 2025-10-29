"""
This module defines the `PhoneNumber` value object, responsible for validating and encapsulating
a properly formatted Nigerian phone number (MSISDN format).

It ensures that phone numbers conform to the international dialing format beginning with
Nigeria’s country code `234`, followed by 10 digits.

Example:
    >>> PhoneNumber("2348031234567")
    <PhoneNumber: 2348031234567>

Classes:
    PhoneNumber: Represents a validated phone number conforming to Termii’s expected format.
"""
import re


class PhoneNumber:
    """
    Represents and validates a phone number in international (MSISDN) format.

    This class enforces that all phone numbers begin with the Nigerian country code `234`
    and are followed by exactly 10 digits, ensuring compatibility with Termii's messaging API
    and other telecom standards.

    Attributes:
        phone_number (str): The validated phone number string in MSISDN format.

    Raises:
        ValueError: If the provided phone number does not match the expected format.
    """

    def __init__(self, phone_number: str):
        """
         Initializes a new `PhoneNumber` instance after validating its format.

        Args:
            phone_number (str): A phone number string in MSISDN format (e.g., "2348031234567").

        Raises:
            ValueError: If the provided phone number is invalid or not in the expected format.

        Example:
            >>> valid = PhoneNumber("2349012345678")
            >>> invalid = PhoneNumber("09012345678")  # Raises ValueError
        """
        if not self.is_valid_phone_number(phone_number):
            raise ValueError(f"Invalid phone number: {phone_number}")
        self.phone_number = phone_number

    @staticmethod
    def is_valid_phone_number(phone_number) -> bool:
        """
        Validates whether the given string is a valid Nigerian phone number in MSISDN format.

        A valid phone number must:
            - Begin with "234" (Nigeria's country code)
            - Contain exactly 13 digits total (234 + 10 digits)
            - Contain only numeric characters

        Args:
            phone_number (str): The phone number string to validate.

        Returns:
            bool: True if the phone number is valid, False otherwise.

        Example:
            >>> PhoneNumber.is_valid_phone_number("2348023456789")
            True
            >>> PhoneNumber.is_valid_phone_number("08023456789")
            False
        """

        return bool(re.match(r"^234\d{10}$", phone_number))
