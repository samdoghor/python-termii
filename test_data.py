from termii_py import TermiiClient

client = TermiiClient()

# message_service = client.message.send_message(
#     sent_to="2348031390921",
#     sent_from="MySenderID",
#     message="Hello, this is a test message.",
#     channel="dnd",
#     type="plain"
# )
#
# print(message_service.status_code)
# print(message_service.status)
# print(message_service.message)


message_number = client.number.send_message(
    sent_to="2348031390921",
    message="Hello, this is a test message.",
)

print(message_number.status_code)
print(message_number.status)
print(message_number.message)