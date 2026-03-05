from termii_py import TermiiClient

client = TermiiClient()

# message_service = client.phonebook.fetch_phonebooks()

message_service = client.contact.create_multiple_contacts(
    phonebook_id="6933004355d9772e0a738ff1",
    file_path="C:/Users/DORGHOR/Documents/Book1.csv",
    country_code="234",
)

print(message_service.status_code)
print(message_service.status)
print(message_service.message)
