"""

"""


class PhonebookService:
    """

    """

    def __init__(self, http):
        """ """

        self.http = http
        
        
    def fetch_phonebooks(self):
        """ """

        return self.http.fetch("/api/phonebooks")

    def create_phonebooks(self, phonebook_name: str, description: str = None):
        """ """

        payload = {
            "phonebook_name": phonebook_name,
            "description": description,
        }

        return self.http.post("/api/phonebooks", json=payload)

    def update_phonebook(self, phonebook_id, phonebook_name: str, description: str):
        """ """

        if not phonebook_id:
            raise ValueError("phonebook_id is required to update a phonebook.")

        payload = {
            "phonebook_name": phonebook_name,
            "description": description,
        }

        return self.http.patch(f"/api/phonebooks/{phonebook_id}", json=payload)

    def delete_phonebook(self, phonebook_id):
        """ """

        if not phonebook_id:
            raise ValueError("phonebook_id is required to delete a phonebook.")

        return self.http.delete(f"/api/phonebooks/{phonebook_id}")
