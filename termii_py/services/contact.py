"""

"""


class ContactService:
    """

    """

    def __init__(self, http):
        """ """

        self.http = http

    def fetch_contacts(self, phonebook_id: str):
        """ """

        if not phonebook_id:
            raise ValueError("phonebook_id is required")

        return self.http.fetch(f"/api/phonebooks/{phonebook_id}/contacts")

    def create_contact(self, phonebook_id, phone_number: str, country_code: str, email_address: str = None, first_name: str = None, last_name: str = None, company: str = None):
        """ """

        if not phonebook_id:
            raise ValueError("phonebook_id is required")

        if country_code.startswith("+"):
            raise ValueError("country code should not start with '+' sign.")

        payload = {
            "phone_number": phone_number,
            "country_code": country_code,
            "email_address": email_address,
            "first_name": first_name,
            "last_name": last_name,
            "company": company,
        }

        return self.http.post(f"/api/phonebooks/{phonebook_id}/contacts", json=payload)

    def create_multiple_contacts(self, phonebook_id, country_code: str, file_path: str,):
        """ """

        if not phonebook_id:
            raise ValueError("phonebook_id is required")

        if country_code.startswith("+"):
            raise ValueError("country code should not start with '+' sign.")

        data = {
            "phonebook_id": phonebook_id,
            "country_code": country_code,
        }

        return self.http.post_file(f"/api/phonebooks/contacts/upload", data=data, file_path=file_path)

    def delete_contact(self, phonebook_id):
        """ """

        if not phonebook_id:
            raise ValueError("phonebook_id is required to delete contacts.")

        return self.http.delete(f"/api/phonebooks/{phonebook_id}/contacts")
