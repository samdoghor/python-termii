import pytest

from termii_py.client import TermiiClient
from termii_py.utils.exception import ClientConfigError


def test_client_uses_direct_credentials(monkeypatch):
    monkeypatch.setattr(
        "termii_py.client.config.TERMII_API_KEY", None, raising=False)
    monkeypatch.setattr(
        "termii_py.client.config.TERMII_BASE_URL", None, raising=False)

    client = TermiiClient(
        api_key="api-key", base_url="https://termii.example/")

    assert client.api_key == "api-key"
    assert client.base_url == "https://termii.example/"
    assert client.http.api_key == "api-key"
    assert client.http.base_url == "https://termii.example"
    assert client.sender_id.http is client.http
    assert client.message.http is client.http
    assert client.number.http is client.http
    assert client.template.http is client.http
    assert client.phonebook.http is client.http
    assert client.contact.http is client.http
    assert client.campaign.http is client.http


def test_client_uses_environment_values(monkeypatch):
    monkeypatch.setattr(
        "termii_py.client.config.TERMII_API_KEY", "env-api-key", raising=False)
    monkeypatch.setattr("termii_py.client.config.TERMII_BASE_URL",
                        "https://env.termii.example/", raising=False)

    client = TermiiClient()

    assert client.api_key == "env-api-key"
    assert client.base_url == "https://env.termii.example/"


def test_client_raises_for_missing_api_key(monkeypatch):
    monkeypatch.setattr(
        "termii_py.client.config.TERMII_API_KEY", None, raising=False)
    monkeypatch.setattr("termii_py.client.config.TERMII_BASE_URL",
                        "https://env.termii.example/", raising=False)

    with pytest.raises(ClientConfigError, match="TERMII_API_KEY"):
        TermiiClient()


def test_client_raises_for_missing_base_url(monkeypatch):
    monkeypatch.setattr(
        "termii_py.client.config.TERMII_API_KEY", "env-api-key", raising=False)
    monkeypatch.setattr(
        "termii_py.client.config.TERMII_BASE_URL", None, raising=False)

    with pytest.raises(ClientConfigError, match="TERMII_BASE_URL"):
        TermiiClient()
