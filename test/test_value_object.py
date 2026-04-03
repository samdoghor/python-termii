import pytest

from termii_py.value_object import PhoneNumber


@pytest.mark.parametrize(
    "phone_number",
    [
        "2348012345678",
        "2349012345678",
    ],
)
def test_phone_number_accepts_valid_msisdn(phone_number):
    value = PhoneNumber(phone_number)

    assert value.phone_number == phone_number
    assert PhoneNumber.is_valid_phone_number(phone_number) is True


@pytest.mark.parametrize(
    "phone_number",
    [
        "08012345678",
        "234801234567",
        "23480123456789",
        "23480abcdef12",
        "",
        None,
    ],
)
def test_phone_number_rejects_invalid_values(phone_number):
    with pytest.raises(ValueError, match="Invalid phone number"):
        PhoneNumber(phone_number)

    assert PhoneNumber.is_valid_phone_number(phone_number) is False
