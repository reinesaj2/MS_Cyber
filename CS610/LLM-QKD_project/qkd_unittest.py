import pytest
from qiskit import QuantumCircuit
from qkd import QuantumProcessor


@pytest.fixture
def processor():
    """Fixture to initialize the QuantumProcessor."""
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


def test_prepare_quantum_state(processor):
    qc_z0 = processor.prepare_quantum_state("0", "Z")
    qc_z1 = processor.prepare_quantum_state("1", "Z")
    qc_x0 = processor.prepare_quantum_state("0", "X")
    qc_x1 = processor.prepare_quantum_state("1", "X")

    assert isinstance(qc_z0, QuantumCircuit)
    assert isinstance(qc_z1, QuantumCircuit)
    assert isinstance(qc_x0, QuantumCircuit)
    assert isinstance(qc_x1, QuantumCircuit)


def test_measure_quantum_state(processor):
    qc_z0 = processor.prepare_quantum_state("0", "Z")
    qc_z1 = processor.prepare_quantum_state("1", "Z")
    qc_x0 = processor.prepare_quantum_state("0", "X")
    qc_x1 = processor.prepare_quantum_state("1", "X")

    result_z0 = processor.measure_quantum_state(qc_z0, "Z")
    result_z1 = processor.measure_quantum_state(qc_z1, "Z")
    result_x0 = processor.measure_quantum_state(qc_x0, "X")
    result_x1 = processor.measure_quantum_state(qc_x1, "X")

    assert result_z0 in ["0", "1"]
    assert result_z1 in ["0", "1"]
    assert result_x0 in ["0", "1"]
    assert result_x1 in ["0", "1"]


def test_generate_shared_key(processor):
    alice_bits = ["0", "1", "0", "1"]
    alice_bases = ["Z", "X", "Z", "X"]
    bob_bases = ["Z", "X", "X", "Z"]
    bob_results = ["0", "1", "0", "1"]

    shared_key = processor.generate_shared_key(
        alice_bits, alice_bases, bob_bases, bob_results
    )
    assert shared_key == "01"


def test_empty_shared_key(processor):
    """
    Test that encryption raises a ValueError when shared key is not set.
    """
    processor.shared_key = None
    with pytest.raises(ValueError, match="Shared key is not initialized."):
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


def test_encrypt_message_without_key(processor):
    with pytest.raises(ValueError, match="Shared key is not initialized."):
        processor.encrypt_message("test")


def test_decrypt_message_without_key(processor):
    with pytest.raises(ValueError, match="Shared key is not initialized."):
        processor.decrypt_message("test")


def test_cleanup(processor):
    processor.cleanup()
    assert not hasattr(processor, "simulator")


if __name__ == "__main__":
    pytest.main()
