from termii_py import TermiiClient

client = TermiiClient()  # when you initialize the client without parameters, it will automatically fetch the API key and base URL from the environment variables if they are set as TERMII_API_KEY and TERMII_BASE_URL respectively.
# client = TermiiClient(api_key="your_api_key", base_url="your_base_url")  # you can also initialize the client with your API key and base URL

# message_service = client.phonebook.fetch_phonebooks()

message_service = client.message.send_message(
    sent_to="2348031390921",
    sent_from="CompanyName",
    message="This is a test message",
    channel="generic",
    type="plain"

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
