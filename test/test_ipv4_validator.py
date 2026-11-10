import pytest
from PySide6.QtGui import QValidator
from source.qt.ipv4_validator import IPv4Validator


@pytest.mark.parametrize(
    "wrong_ip_addr",
    [
        "256.0.0.0",
        "0.256.0.0",
        "0.0.256.0",
        "0.0.0.256",
    ],
)

def test_outrange_octet(wrong_ip_addr):
    validator = IPv4Validator()

    expected, _, _ = validator.validate(wrong_ip_addr, 0)

    assert expected == QValidator.State.Invalid