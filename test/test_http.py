from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

from termii_py.http import RequestHandler, RequestResponse


def test_fetch_adds_api_key_and_strips_trailing_slash():
    handler = RequestHandler("secret-key", "https://termii.example/")
    response = SimpleNamespace(status_code=200, text="ok")

    with patch("termii_py.http.request_handler.requests.get", return_value=response) as mock_get:
        with patch("termii_py.http.request_handler.RequestResponse.handle_response", return_value="handled") as mock_handle:
            result = handler.fetch("/api/items", params={"page": 1})

    assert result == "handled"
    mock_get.assert_called_once_with(
        "https://termii.example/api/items",
        params={"page": 1, "api_key": "secret-key"},
    )
    mock_handle.assert_called_once_with(response)


def test_post_adds_api_key():
    handler = RequestHandler("secret-key", "https://termii.example")
    response = SimpleNamespace(status_code=201, text="created")

    with patch("termii_py.http.request_handler.requests.post", return_value=response) as mock_post:
        with patch("termii_py.http.request_handler.RequestResponse.handle_response", return_value="handled") as mock_handle:
            result = handler.post("/api/items", json={"name": "demo"})

    assert result == "handled"
    mock_post.assert_called_once_with(
        "https://termii.example/api/items",
        json={"name": "demo", "api_key": "secret-key"},
    )
    mock_handle.assert_called_once_with(response)


def test_patch_adds_api_key():
    handler = RequestHandler("secret-key", "https://termii.example")
    response = SimpleNamespace(status_code=200, text="updated")

    with patch("termii_py.http.request_handler.requests.patch", return_value=response) as mock_patch:
        with patch("termii_py.http.request_handler.RequestResponse.handle_response", return_value="handled") as mock_handle:
            result = handler.patch("/api/items/1", json={"name": "demo"})

    assert result == "handled"
    mock_patch.assert_called_once_with(
        "https://termii.example/api/items/1",
        json={"name": "demo", "api_key": "secret-key"},
    )
    mock_handle.assert_called_once_with(response)


def test_delete_adds_api_key():
    handler = RequestHandler("secret-key", "https://termii.example")
    response = SimpleNamespace(status_code=200, text="deleted")

    with patch("termii_py.http.request_handler.requests.delete", return_value=response) as mock_delete:
        with patch("termii_py.http.request_handler.RequestResponse.handle_response", return_value="handled") as mock_handle:
            result = handler.delete("/api/items/1", params={"force": True})

    assert result == "handled"
    mock_delete.assert_called_once_with(
        "https://termii.example/api/items/1",
        params={"force": True, "api_key": "secret-key"},
    )
    mock_handle.assert_called_once_with(response)


def test_post_file_uses_file_upload_and_closes_file(tmp_path: Path):
    handler = RequestHandler("secret-key", "https://termii.example")
    file_path = tmp_path / "contacts.csv"
    file_path.write_text("phone_number\n2348012345678\n", encoding="utf-8")
    response = SimpleNamespace(status_code=200, text="uploaded")

    with patch("termii_py.http.request_handler.requests.post", return_value=response) as mock_post:
        with patch("termii_py.http.request_handler.RequestResponse.handle_response", return_value="handled") as mock_handle:
            result = handler.post_file(
                "/api/upload", str(file_path), {"phonebook_id": "abc123"})

    assert result == "handled"
    files = mock_post.call_args.kwargs["files"]
    data = mock_post.call_args.kwargs["data"]
    assert data == {"phonebook_id": "abc123", "api_key": "secret-key"}
    assert files["file"].closed is True
    mock_handle.assert_called_once_with(response)


def test_request_response_marks_success_and_error():
    ok_response = SimpleNamespace(
        status_code=200, text="{""status"": ""success""}")
    created_response = SimpleNamespace(
        status_code=201, text="{""status"": ""created""}")
    error_response = SimpleNamespace(status_code=400, text="bad request")

    ok_result = RequestResponse.handle_response(ok_response)
    created_result = RequestResponse.handle_response(created_response)
    error_result = RequestResponse.handle_response(error_response)

    assert ok_result.status_code == 200
    assert ok_result.status == "ok"
    assert ok_result.message == ok_response.text
    assert created_result.status_code == 201
    assert created_result.status == "ok"
    assert created_result.message == created_response.text
    assert error_result.status_code == 400
    assert error_result.status == "error"
    assert error_result.message == "bad request"
