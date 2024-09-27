import pytest
from qiskit_ibm_provider import IBMProvider
from qkd import QuantumProcessor


@pytest.fixture
def processor():
    """Fixture to initialize the QuantumProcessor with an IBMProvider."""
    # Load IBM Quantum account (make sure to have your IBM Quantum account set up)
    provider = IBMProvider()
    return QuantumProcessor(provider)


def test_prepare_qubit_state(processor):
    """
    Test qubit state preparation for both bit values and bases.
    """
    # Test for bit=0 in Z basis
    qc_z0 = processor.prepare_qubit_state(bit=0, basis='Z')
    assert qc_z0 is not None, "QuantumCircuit for bit=0 in Z basis should not be None."

    # Test for bit=1 in Z basis
    qc_z1 = processor.prepare_qubit_state(bit=1, basis='Z')
    assert qc_z1 is not None, "QuantumCircuit for bit=1 in Z basis should not be None."

    # Test for bit=0 in X basis
    qc_x0 = processor.prepare_qubit_state(bit=0, basis='X')
    assert qc_x0 is not None, "QuantumCircuit for bit=0 in X basis should not be None."

    # Test for bit=1 in X basis
    qc_x1 = processor.prepare_qubit_state(bit=1, basis='X')
    assert qc_x1 is not None, "QuantumCircuit for bit=1 in X basis should not be None."


def test_measure_qubit_state(processor):
    """
    Test the measurement of qubit states in different bases.
    """
    # Prepare a qubit in state |0> and measure in Z basis
    qc = processor.prepare_qubit_state(bit=0, basis='Z')
    result = processor.measure_qubit_state(qc, basis='Z')
    assert result in [0, 1], "Measurement result should be 0 or 1."

    # Prepare a qubit in state |1> and measure in X basis
    qc = processor.prepare_qubit_state(bit=1, basis='X')
    result = processor.measure_qubit_state(qc, basis='X')
    assert result in [0, 1], "Measurement result should be 0 or 1."


def test_generate_shared_key(processor):
    """
    Test the shared key generation between Alice and Bob.
    """
    # Simulate Alice's bits and bases
    alice_bits = [0, 1, 0, 1]
    alice_bases = ['Z', 'X', 'Z', 'X']

    # Simulate Bob's bases and results
    processor.bob_bases = ['Z', 'X', 'X', 'X']
    processor.bob_results = [0, 1, 0, 1]

    # Generate shared key on client side (Alice)
    matching_indices = processor.generate_shared_key_client(
        alice_bits, alice_bases, processor.bob_bases, processor.bob_results
    )
    assert matching_indices == [0, 1, 3], "Matching indices should be [0, 1, 3]."
    assert processor.shared_key == '011', "Shared key should be '011'."

    # Generate shared key on server side (Bob)
    shared_key_server = processor.generate_shared_key_server(matching_indices)
    assert shared_key_server == '001', "Bob's shared key should be '001'."

    # In a real scenario, Alice and Bob should reconcile the key through error correction


def test_encrypt_decrypt_message(processor):
    """
    Test encryption and decryption of a message using the shared key.
    """
    # Set a shared key for testing
    processor.shared_key = '0110'
    message = "Test Message"

    encrypted_message = processor.encrypt_message(message)
    assert encrypted_message != message, "Encrypted message should not be the same as the original message."

    decrypted_message = processor.decrypt_message(encrypted_message)
    assert decrypted_message == message, "Decrypted message should match the original message."


def test_encrypt_message_without_key(processor):
    """
    Test that encryption raises a ValueError when shared key is not set.
    """
    processor.shared_key = None
    with pytest.raises(ValueError, match="Shared key is not initialized."):
        processor.encrypt_message("Hello")


def test_cleanup(processor):
    """
    Test the cleanup method to ensure resources are released.
    """
    processor.cleanup()
    assert not hasattr(processor, "backend"), "Backend should be deleted after cleanup."


if __name__ == "__main__":
    pytest.main()
