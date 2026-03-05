# python-termii

A clean and lightweight Python SDK for [Termii](https://termii.com) — send SMS, WhatsApp messages, manage phonebooks,
contacts, campaigns, and more.

[![PyPI version](https://img.shields.io/pypi/v/python-termii)](https://pypi.org/project/python-termii/)
[![Python](https://img.shields.io/pypi/pyversions/python-termii)](https://pypi.org/project/python-termii/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Development Status](https://img.shields.io/badge/status-alpha-orange)](https://pypi.org/project/python-termii/)

---

## Table of Contents

- [Installation](#installation)
- [Configuration](#configuration)
- [Services](#services)
    - [Sender ID](#sender-id)
    - [Messaging](#messaging)
    - [Number](#number)
    - [Template](#template)
    - [Phonebook](#phonebook)
    - [Contact](#contact)
    - [Campaign](#campaign)
- [Error Handling](#error-handling)
- [Contributing](#contributing)
- [License](#license)

---

## Installation

```bash
pip install python-termii
```

---

## Configuration

Initialize the client with your API key and base URL. Both can be passed directly or loaded from environment variables.

```python
from termii_py import TermiiClient

# Pass credentials directly
client = TermiiClient(api_key="YOUR_API_KEY", base_url="YOUR_BASE_URL")

# Or set environment variables and call with no arguments
client = TermiiClient()
```

**Using a `.env` file (recommended):**

```env
TERMII_API_KEY=your_api_key
TERMII_BASE_URL=your_base_url
```

```python
from termii_py import TermiiClient

client = TermiiClient()
```

> Get your API key and base URL from your [Termii dashboard](https://app.termii.com). A `ClientConfigError` is raised if
> either value is missing.

---

## Services

All services are available as attributes on the `TermiiClient` instance.

### Sender ID

**Fetch sender IDs** — optionally filter by name or status:

```python
# Fetch all
client.sender_id.fetch_id()

# Filter by name or status
client.sender_id.fetch_id(name="MyBrand", status="approved")
```

**Request a new sender ID:**

```python
client.sender_id.request_id(
    sender_id="MyBrand",
    usecase="Transactional alerts for order confirmations",
    company="Acme Ltd"
)
```

---

### Messaging

**Send a single SMS:**

```python
client.message.send_message(
    sent_to="2348012345678",
    sent_from="MyBrand",
    message="Your order has been confirmed.",
    channel="generic",  # "generic", "dnd", or "voice"
    type="plain"
)
```

> For voice channel, `type` must be `"voice"`. WhatsApp messages must use `send_whatsapp_message()`.

**Send a WhatsApp message:**

```python
# Text only
client.message.send_whatsapp_message(
    sent_to="2348012345678",
    sent_from="MyBrand",
    message="Hello! Your appointment is confirmed."
)

# With media attachment
client.message.send_whatsapp_message(
    sent_to="2348012345678",
    sent_from="MyBrand",
    message="Here is your receipt.",
    url="https://example.com/receipt.pdf",
    caption="Receipt - March 2025"
)
```

**Send a bulk SMS:**

```python
client.message.send_bulk_message(
    sent_to=["2348012345678", "2349087654321"],
    sent_from="MyBrand",
    message="Our sale starts today!",
    channel="generic",  # "generic" or "dnd" only
    type="plain"
)
```

> Voice and WhatsApp are not supported for bulk messaging.

---

### Number

Send a message directly to a phone number without a sender ID:

```python
client.number.send_message(
    sent_to="2348012345678",
    message="Your verification code is 123456."
)
```

---

### Template

Send a message using a pre-approved WhatsApp template:

```python
# Text template
client.template.send_message(
    sent_to="2348012345678",
    device_id="your-device-id",
    template_id="your-template-id",
    data={"studname": "Victor", "average": "30"}
)

# Media template (url and caption must be provided together)
client.template.send_message(
    sent_to="2348012345678",
    device_id="your-device-id",
    template_id="your-template-id",
    data={"name": "Victor"},
    url="https://example.com/document.pdf",
    caption="Course Result"
)
```

> `device_id` is found on the Manage Device page of your Termii dashboard.

---

### Phonebook

**Fetch all phonebooks:**

```python
client.phonebook.fetch_phonebooks()
```

**Create a phonebook:**

```python
client.phonebook.create_phonebooks(
    phonebook_name="Newsletter Subscribers",
    description="Users opted in for weekly updates"
)
```

**Update a phonebook:**

```python
client.phonebook.update_phonebook(
    phonebook_id="abc123",
    phonebook_name="VIP Customers",
    description="High-value customer segment"
)
```

**Delete a phonebook:**

```python
client.phonebook.delete_phonebook(phonebook_id="abc123")
```

---

### Contact

**Fetch contacts in a phonebook:**

```python
client.contact.fetch_contacts(phonebook_id="abc123")
```

**Add a single contact:**

```python
client.contact.create_contact(
    phonebook_id="abc123",
    phone_number="8012345678",
    country_code="234",  # No leading "+"
    first_name="Ada",
    last_name="Obi",
    email_address="ada@example.com",
    company="Acme Ltd"
)
```

**Add multiple contacts via CSV upload:**

```python
client.contact.create_multiple_contacts(
    phonebook_id="abc123",
    country_code="234",  # No leading "+"
    file_path="/path/to/contacts.csv"
)
```

**Delete all contacts in a phonebook:**

```python
client.contact.delete_contact(phonebook_id="abc123")
```

> ⚠️ `delete_contact` removes **all** contacts in the specified phonebook. Use with caution.

---

### Campaign

**Send a campaign:**

```python
# Send immediately
client.campaign.send_campaign(
    country_code="234",  # No leading "+"
    sender_id="MyBrand",  # 3–11 characters
    message="Big sale — ends tonight!",
    message_type="plain",  # "plain" or "unicode"
    phonebook_id="abc123",
    enable_link_tracking=False,
    campaign_type="promotional",
    schedule_sms_status="regular",  # "regular" or "scheduled"
    channel="dnd"  # "dnd" or "generic"
)

# Schedule for later
client.campaign.send_campaign(
    country_code="234",
    sender_id="MyBrand",
    message="Your monthly statement is ready.",
    message_type="plain",
    phonebook_id="abc123",
    enable_link_tracking=True,
    campaign_type="transactional",
    schedule_sms_status="scheduled",
    schedule_time="2025-12-31T23:59:00Z",  # Required when schedule_sms_status is "scheduled"
    channel="dnd"
)
```

**Fetch all campaigns:**

```python
client.campaign.fetch_campaigns()
```

**Fetch a specific campaign's history:**

```python
client.campaign.fetch_campaign_history(campaign_id="camp_xyz")
```

**Retry a failed campaign:**

```python
client.campaign.retry_campaign(campaign_id="camp_xyz")
```

---

## Error Handling

The SDK validates inputs before making any network call and raises `ValueError` for invalid parameters. Wrap calls
accordingly:

```python
try:
    response = client.message.send_message(
        sent_to="2348012345678",
        sent_from="MyBrand",
        message="Hello!",
        channel="generic",
        type="plain"
    )
except ValueError as e:
    print(f"Validation error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

---

## Contributing

Contributions are welcome!

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m "feat: describe your change"`
4. Push: `git push origin feature/your-feature`
5. Open a Pull Request

Please open an issue first for significant changes.

---

## License

This project is licensed under the [MIT License](LICENSE).

---

Built by [Samuel Doghor](https://github.com/samdoghor) · Powered by the [Termii API](https://developer.termii.com)