import pytest
from qkd import QuantumProcessor


@pytest.fixture
def processor():
    """Fixture to initialize the QuantumCryptographyProcessor."""
    return QuantumProcessor()


@pytest.mark.parametrize(
    "message, shared_key",
    [
        ("Hello", "01010101"),  # Standard ASCII characters with an 8-bit key
        ("Secret123", "1010101010101010"),  # Alphanumeric with a 16-bit key
        ("!@#$$%^&*", "111000111"),  # Special characters with a 9-bit key
        ("こんにちは", "10101"),  # Unicode (Japanese) characters with a 5-bit key
        ("", "01010101"),  # Edge case: empty message
    ],
)
def test_encrypt_decrypt_message(processor, message, shared_key):
    """
    Test encryption and decryption of messages with different key lengths and message types.
    """
    processor.shared_key = shared_key
    encrypted_message = processor.encrypt_message(message)
    decrypted_message = processor.decrypt_message(encrypted_message)

    if message:  # Only assert message modification if message is not empty
        assert (
            message != encrypted_message
        ), "Encryption should modify the original message."
    else:
        assert encrypted_message == "", "Encrypted empty message should remain empty."

    assert message == decrypted_message, "Decrypted message should match the original."


def test_empty_shared_key(processor):
    """
    Test that encryption raises a ValueError when shared key is not set.
    """
    processor.shared_key = None
    with pytest.raises(ValueError, match="Shared key is not set"):
        processor.encrypt_message("Hello")


def test_invalid_shared_key_length(processor):
    """
    Test that encryption handles cases where shared key length does not match message length.
    """
    processor.shared_key = "1"  # Single-bit shared key
    message = "Test"
    encrypted_message = processor.encrypt_message(message)
    decrypted_message = processor.decrypt_message(encrypted_message)

    assert (
        message != encrypted_message
    ), "Encryption should modify the message even with a short key."
    assert (
        message == decrypted_message
    ), "Decrypted message should still match the original."


def test_non_ascii_characters(processor):
    """
    Test encryption and decryption with non-ASCII (Unicode) characters.
    """
    processor.shared_key = "10101"  # Use a simple 5-bit key
    message = "こんにちは"  # Japanese greeting (non-ASCII characters)
    encrypted_message = processor.encrypt_message(message)
    decrypted_message = processor.decrypt_message(encrypted_message)

    assert (
        message != encrypted_message
    ), "Non-ASCII message should be modified by encryption."
    assert (
        message == decrypted_message
    ), "Decrypted message should match the original non-ASCII message."


def test_empty_message(processor):
    """
    Test encryption and decryption of an empty message.
    """
    processor.shared_key = "10101010"  # Set a shared key
    message = ""  # Empty message
    encrypted_message = processor.encrypt_message(message)
    decrypted_message = processor.decrypt_message(encrypted_message)

    assert encrypted_message == "", "Encrypted empty message should remain empty."
    assert decrypted_message == "", "Decrypted empty message should remain empty."


if __name__ == "__main__":
    pytest.main()
