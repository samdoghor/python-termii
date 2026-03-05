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

# message_service = client.template.send_message(
#     sent_to="2348031390921",
#     device_id="f3f4f7b0-52d8-40bc-91fc-120da11ff936",
#     template_id="1493-csdn3-ns34w-sd3434-dfdf",
#     data={
#         "product_name": "Termii",
#         "otp": 120435,
#         "expiry_time": "10 minutes"
#     },
#     caption="We are excited to have you on board!",
#     url="https://example.com/welcome-image.jpg"
# )
#
# print(message_service.status_code)
# print(message_service.status)
# print(message_service.message)

# import requests
#
# from termii_py import config
#
# url = f"https://{config.TERMII_BASE_URL}/api/send/template"
# payload = {
#     "phone_number": "2348031390921",
#     "device_id": "f3f4f7b0-52d8-40bc-91fc-120da11ff936",
#     "template_id": "1493-csdn3-ns34w-sd3434-dfdf",
#     "data": {
#         "product_name": "Termii",
#         "otp": 120435,
#         "expiry_time": "10 minutes"
#     },
#     "api_key": config.TERMII_API_KEY
# }
#
# headers = {
#     'Content-Type': 'application/json',
# }
# response = requests.request("POST", url, headers=headers, json=payload)
# print(response.text)
