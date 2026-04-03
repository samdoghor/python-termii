from unittest.mock import MagicMock

import pytest

from termii_py.services.campaign import CampaignService
from termii_py.services.contact import ContactService
from termii_py.services.message import MessageService
from termii_py.services.number import NumberService
from termii_py.services.phonebook import PhonebookService
from termii_py.services.sender_id import SenderIDService
from termii_py.services.template import TemplateService


def make_http_mock():
    return MagicMock()


def test_sender_id_fetch_id_uses_optional_filters():
    http = make_http_mock()
    http.fetch.return_value = "ok"
    service = SenderIDService(http)

    result = service.fetch_id(name="MyBrand", status="approved")

    assert result == "ok"
    http.fetch.assert_called_once_with(
        "/api/sender-id", params={"name": "MyBrand", "status": "approved"})


def test_sender_id_request_id_builds_payload():
    http = make_http_mock()
    http.post.return_value = "ok"
    service = SenderIDService(http)

    result = service.request_id("MyBrand", "Transactional alerts", "Acme Ltd")

    assert result == "ok"
    http.post.assert_called_once_with(
        "/api/sender-id/request",
        json={"sender_id": "MyBrand",
              "usecase": "Transactional alerts", "company": "Acme Ltd"},
    )


def test_message_send_message_allows_generic_and_voice():
    http = make_http_mock()
    http.post.return_value = "ok"
    service = MessageService(http)

    result = service.send_message(
        sent_to="2348012345678",
        sent_from="MyBrand",
        message="Your order has been confirmed.",
        channel="generic",
        type="plain",
    )

    assert result == "ok"
    http.post.assert_called_once_with(
        "/api/sms/send",
        json={
            "to": "2348012345678",
            "from": "MyBrand",
            "sms": "Your order has been confirmed.",
            "channel": "generic",
            "type": "plain",
        },
    )


def test_message_send_message_allows_voice_when_type_matches():
    http = make_http_mock()
    http.post.return_value = "ok"
    service = MessageService(http)

    result = service.send_message(
        sent_to="2348012345678",
        sent_from="MyBrand",
        message="Press 1 to confirm.",
        channel="voice",
        type="voice",
    )

    assert result == "ok"
    http.post.assert_called_once()


@pytest.mark.parametrize(
    "channel, message_type, error_message",
    [
        ("whatsapp", "plain", "For WhatsApp messages"),
        ("voice", "plain", "For voice channel"),
        ("invalid", "plain", "must be either 'generic' or 'dnd' or voice"),
    ],
)
def test_message_send_message_validates_channel(channel, message_type, error_message):
    http = make_http_mock()
    service = MessageService(http)

    with pytest.raises(ValueError, match=error_message):
        service.send_message(
            sent_to="2348012345678",
            sent_from="MyBrand",
            message="Hello",
            channel=channel,
            type=message_type,
        )


def test_message_send_whatsapp_message_builds_payload():
    http = make_http_mock()
    http.post.return_value = "ok"
    service = MessageService(http)

    result = service.send_whatsapp_message(
        sent_to="2348012345678",
        sent_from="MyBrand",
        message="Hello!",
    )

    assert result == "ok"
    http.post.assert_called_once_with(
        "/api/sms/send",
        json={
            "to": "2348012345678",
            "from": "MyBrand",
            "sms": "Hello!",
            "channel": "whatsapp",
            "type": "plain",
            "media": {"url": None, "caption": None},
        },
    )


def test_message_send_bulk_message_builds_payload():
    http = make_http_mock()
    http.post.return_value = "ok"
    service = MessageService(http)

    result = service.send_bulk_message(
        sent_to=["2348012345678", "2348098765432"],
        sent_from="MyBrand",
        message="Promo",
        channel="dnd",
        type="plain",
    )

    assert result == "ok"
    http.post.assert_called_once_with(
        "/api/sms/send/bulk",
        json={
            "to": ["2348012345678", "2348098765432"],
            "from": "MyBrand",
            "sms": "Promo",
            "channel": "dnd",
            "type": "plain",
        },
    )


@pytest.mark.parametrize(
    "channel, message_type, error_message",
    [
        ("whatsapp", "plain", "For WhatsApp messages"),
        ("voice", "plain", "Voice messages are not supported in bulk messaging."),
        ("generic", "voice", "Voice messages are not supported in bulk messaging."),
        ("invalid", "plain", "must be either 'generic' or 'dnd' or voice"),
    ],
)
def test_message_send_bulk_message_validates_channel(channel, message_type, error_message):
    http = make_http_mock()
    service = MessageService(http)

    with pytest.raises(ValueError, match=error_message):
        service.send_bulk_message(
            sent_to=["2348012345678"],
            sent_from="MyBrand",
            message="Promo",
            channel=channel,
            type=message_type,
        )


def test_number_send_message_builds_payload():
    http = make_http_mock()
    http.post.return_value = "ok"
    service = NumberService(http)

    result = service.send_message(
        sent_to="2348012345678", message="Your code is 123456")

    assert result == "ok"
    http.post.assert_called_once_with(
        "/api/sms/number/send",
        json={"to": "2348012345678", "sms": "Your code is 123456"},
    )


def test_template_send_message_builds_text_payload():
    http = make_http_mock()
    http.post.return_value = "ok"
    service = TemplateService(http)

    result = service.send_message(
        sent_to="2348012345678",
        device_id="device-1",
        template_id="template-1",
        data={"name": "Ada"},
    )

    assert result == "ok"
    http.post.assert_called_once_with(
        "/api/send/template",
        json={
            "phone_number": "2348012345678",
            "device_id": "device-1",
            "template_id": "template-1",
            "data": {"name": "Ada"},
        },
    )


def test_template_send_message_builds_media_payload():
    http = make_http_mock()
    http.post.return_value = "ok"
    service = TemplateService(http)

    result = service.send_message(
        sent_to="2348012345678",
        device_id="device-1",
        template_id="template-1",
        data={"name": "Ada"},
        caption="Receipt",
        url="https://example.com/receipt.pdf",
    )

    assert result == "ok"
    http.post.assert_called_once_with(
        "/api/send/template/media",
        json={
            "phone_number": "2348012345678",
            "device_id": "device-1",
            "template_id": "template-1",
            "data": {"name": "Ada"},
            "media": {"caption": "Receipt", "url": "https://example.com/receipt.pdf"},
        },
    )


@pytest.mark.parametrize(
    "caption, url, error_message",
    [
        ("Receipt", None, "If caption is provided, url must also be provided"),
        (None, "https://example.com/receipt.pdf",
         "If url is provided, caption must also be provided"),
        (None, None, None),
    ],
)
def test_template_send_message_validates_media_arguments(caption, url, error_message):
    http = make_http_mock()
    service = TemplateService(http)

    if error_message:
        with pytest.raises(ValueError, match=error_message):
            service.send_message(
                sent_to="2348012345678",
                device_id="device-1",
                template_id="template-1",
                data={"name": "Ada"},
                caption=caption,
                url=url,
            )
    else:
        service.send_message(
            sent_to="2348012345678",
            device_id="device-1",
            template_id="template-1",
            data={"name": "Ada"},
        )


def test_template_send_message_requires_dict_data():
    http = make_http_mock()
    service = TemplateService(http)

    with pytest.raises(ValueError, match="The 'data' parameter must be a dictionary"):
        service.send_message(
            sent_to="2348012345678",
            device_id="device-1",
            template_id="template-1",
            data=["not", "a", "dict"],
        )


def test_phonebook_methods_delegate_to_http():
    http = make_http_mock()
    http.fetch.return_value = "fetched"
    http.post.return_value = "created"
    http.patch.return_value = "updated"
    http.delete.return_value = "deleted"
    service = PhonebookService(http)

    assert service.fetch_phonebooks() == "fetched"
    assert service.create_phonebooks(
        "Newsletter", "Weekly updates") == "created"
    assert service.update_phonebook(
        "pb-1", "VIP", "Top customers") == "updated"
    assert service.delete_phonebook("pb-1") == "deleted"

    http.fetch.assert_called_once_with("/api/phonebooks")
    http.post.assert_called_once_with(
        "/api/phonebooks",
        json={"phonebook_name": "Newsletter", "description": "Weekly updates"},
    )
    http.patch.assert_called_once_with(
        "/api/phonebooks/pb-1",
        json={"phonebook_name": "VIP", "description": "Top customers"},
    )
    http.delete.assert_called_once_with("/api/phonebooks/pb-1")


def test_phonebook_update_and_delete_require_ids():
    http = make_http_mock()
    service = PhonebookService(http)

    with pytest.raises(ValueError, match="phonebook_id is required to update a phonebook"):
        service.update_phonebook("", "VIP", "Top customers")

    with pytest.raises(ValueError, match="phonebook_id is required to delete a phonebook"):
        service.delete_phonebook(None)


def test_contact_methods_delegate_to_http():
    http = make_http_mock()
    http.fetch.return_value = "contacts"
    http.post.return_value = "created"
    http.post_file.return_value = "uploaded"
    http.delete.return_value = "deleted"
    service = ContactService(http)

    assert service.fetch_contacts("pb-1") == "contacts"
    assert service.create_contact(
        "pb-1",
        phone_number="8012345678",
        country_code="234",
        email_address="ada@example.com",
        first_name="Ada",
        last_name="Obi",
        company="Acme Ltd",
    ) == "created"
    assert service.create_multiple_contacts(
        "pb-1", "234", "contacts.csv") == "uploaded"
    assert service.delete_contact("pb-1") == "deleted"

    http.fetch.assert_called_once_with("/api/phonebooks/pb-1/contacts")
    http.post.assert_called_once_with(
        "/api/phonebooks/pb-1/contacts",
        json={
            "phone_number": "8012345678",
            "country_code": "234",
            "email_address": "ada@example.com",
            "first_name": "Ada",
            "last_name": "Obi",
            "company": "Acme Ltd",
        },
    )
    http.post_file.assert_called_once_with(
        "/api/phonebooks/contacts/upload",
        data={"phonebook_id": "pb-1", "country_code": "234"},
        file_path="contacts.csv",
    )
    http.delete.assert_called_once_with("/api/phonebooks/pb-1/contacts")


@pytest.mark.parametrize(
    "method_name, args, error_message",
    [
        ("fetch_contacts", {"phonebook_id": ""}, "phonebook_id is required"),
        ("create_contact", {"phonebook_id": "", "phone_number": "8012345678",
         "country_code": "234"}, "phonebook_id is required"),
        ("create_contact", {"phonebook_id": "pb-1", "phone_number": "8012345678",
         "country_code": "+234"}, "country code should not start"),
        ("create_multiple_contacts", {"phonebook_id": "", "country_code": "234",
         "file_path": "contacts.csv"}, "phonebook_id is required"),
        ("create_multiple_contacts", {"phonebook_id": "pb-1", "country_code": "+234",
         "file_path": "contacts.csv"}, "country code should not start"),
        ("delete_contact", {"phonebook_id": ""},
         "phonebook_id is required to delete contacts"),
    ],
)
def test_contact_methods_validate_inputs(method_name, args, error_message):
    http = make_http_mock()
    service = ContactService(http)

    with pytest.raises(ValueError, match=error_message):
        getattr(service, method_name)(**args)


def test_campaign_send_campaign_builds_payload():
    http = make_http_mock()
    http.post.return_value = "ok"
    service = CampaignService(http)

    result = service.send_campaign(
        country_code="234",
        sender_id="MyBrand",
        message="Big sale",
        message_type="plain",
        phonebook_id="pb-1",
        enable_link_tracking=False,
        campaign_type="promotional",
        schedule_sms_status="regular",
        channel="dnd",
    )

    assert result == "ok"
    http.post.assert_called_once_with(
        "/api/sms/campaigns/send",
        {
            "country_code": "234",
            "sender_id": "MyBrand",
            "message": "Big sale",
            "message_type": "plain",
            "phonebook_id": "pb-1",
            "enable_link_tracking": False,
            "campaign_type": "promotional",
            "schedule_sms_status": "regular",
            "schedule_time": None,
            "channel": "dnd",
            "remove_duplicate": "yes",
            "delimiter": ",",
        },
    )


def test_campaign_send_campaign_requires_schedule_time_when_scheduled():
    http = make_http_mock()
    service = CampaignService(http)

    with pytest.raises(ValueError, match="schedule time is required"):
        service.send_campaign(
            country_code="234",
            sender_id="MyBrand",
            message="Big sale",
            message_type="plain",
            phonebook_id="pb-1",
            enable_link_tracking=False,
            campaign_type="promotional",
            schedule_sms_status="scheduled",
            channel="dnd",
        )


@pytest.mark.parametrize(
    "kwargs, error_message",
    [
        ({"country_code": "+234"}, "country code should not start"),
        ({"sender_id": "AB"}, "sender id should be between 3 and 11 characters"),
        ({"message_type": "emoji"},
         "message type should be either 'plain' or 'unicode'"),
        ({"channel": "voice"}, "channel should be either 'dnd' or 'generic'"),
        ({"schedule_sms_status": "later"},
         "schedule sms status should be either 'scheduled' or 'regular'"),
    ],
)
def test_campaign_send_campaign_validates_inputs(kwargs, error_message):
    http = make_http_mock()
    service = CampaignService(http)

    base_kwargs = {
        "country_code": "234",
        "sender_id": "MyBrand",
        "message": "Big sale",
        "message_type": "plain",
        "phonebook_id": "pb-1",
        "enable_link_tracking": False,
        "campaign_type": "promotional",
        "schedule_sms_status": "regular",
        "channel": "dnd",
    }
    base_kwargs.update(kwargs)

    with pytest.raises(ValueError, match=error_message):
        service.send_campaign(**base_kwargs)


def test_campaign_fetch_and_retry_methods_delegate_to_http():
    http = make_http_mock()
    http.fetch.return_value = "campaigns"
    http.patch.return_value = "retried"
    service = CampaignService(http)

    assert service.fetch_campaigns() == "campaigns"
    assert service.fetch_campaign_history("camp-1") == "campaigns"
    assert service.retry_campaign("camp-1") == "retried"

    http.fetch.assert_any_call("/api/sms/campaigns")
    http.fetch.assert_any_call("/api/sms/campaigns/camp-1")
    http.patch.assert_called_once_with("/api/sms/campaigns/camp-1", json={})


@pytest.mark.parametrize(
    "method_name, kwargs, error_message",
    [
        ("fetch_campaign_history", {
         "campaign_id": ""}, "campaign id is required"),
        ("retry_campaign", {"campaign_id": None}, "campaign id is required"),
    ],
)
def test_campaign_campaign_id_is_required(method_name, kwargs, error_message):
    http = make_http_mock()
    service = CampaignService(http)

    with pytest.raises(ValueError, match=error_message):
        getattr(service, method_name)(**kwargs)
