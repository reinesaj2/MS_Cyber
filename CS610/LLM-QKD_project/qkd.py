from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
import numpy as np

class QuantumProcessor:
    """
    QuantumProcessor simulates the BB84 Quantum Key Distribution (QKD) protocol.
    It handles quantum state preparation, measurement, key generation, and message encryption/decryption.
    """

    def __init__(self):
        """
        Initialize the QuantumProcessor with a quantum simulator and empty shared key.
        """
        self.shared_key = None
        self.simulator = AerSimulator()

    def prepare_quantum_state(self, bit, basis):
        """
        Prepare the quantum state based on the given bit and basis.

        :param bit: The classical bit (0 or 1) to encode into the quantum state.
        :param basis: The basis to use for encoding ('Z' for rectilinear or 'X' for diagonal).
        :return: A QuantumCircuit object representing the prepared quantum state.
        """
        qc = QuantumCircuit(1, 1)
        if bit == '1':
            qc.x(0)  # Apply X gate to encode bit 1
        if basis == 'X':
            qc.h(0)  # Apply H gate for diagonal basis
        return qc

    def measure_quantum_state(self, qc, basis):
        """
        Measure the quantum state based on the given measurement basis.

        :param qc: The QuantumCircuit containing the quantum state.
        :param basis: The basis to measure in ('Z' for rectilinear or 'X' for diagonal).
        :return: The measured classical bit (0 or 1).
        """
        if basis == 'X':
            qc.h(0)  # Apply H gate to switch to diagonal basis for measurement
        qc.measure(0, 0)
        job = transpile(qc, self.simulator)
        result = self.simulator.run(job, shots=1).result()
        counts = result.get_counts()
        return '1' if '1' in counts else '0'

    def generate_shared_key(self, alice_bits, alice_bases, bob_bases, bob_results):
        """
        Generate a shared key using the BB84 protocol by comparing Alice's and Bob's bases.

        :param alice_bits: The bits prepared by Alice.
        :param alice_bases: The bases used by Alice to encode the bits.
        :param bob_bases: The bases used by Bob to measure the qubits.
        :param bob_results: The measurement results obtained by Bob.
        :return: The sifted shared key.
        """
        sifted_key = [
            alice_bit for alice_bit, alice_base, bob_base, bob_result
            in zip(alice_bits, alice_bases, bob_bases, bob_results)
            if alice_base == bob_base  # Only keep the bits where bases match
        ]
        self.shared_key = ''.join(sifted_key)
        print(f"Shared key generated: {self.shared_key}")  # Debugging line
        return self.shared_key

    def encrypt_message(self, message):
        """
        Encrypt a message using the shared key.

        :param message: The plaintext message to be encrypted.
        :return: The encrypted message as a string.
        :raises ValueError: If the shared key is not set.
        """
        if self.shared_key is None:
            raise ValueError("Shared key is not initialized.")
        
        # Encrypt using XOR with the shared key
        encrypted_message = ''.join(
            chr(ord(c) ^ int(self.shared_key[i % len(self.shared_key)], 2))
            for i, c in enumerate(message)
        )
        print(f"Encrypted message: {encrypted_message}")  # Debugging line
        return encrypted_message

    def decrypt_message(self, encrypted_message):
        """
        Decrypt an encrypted message using the shared key.

        :param encrypted_message: The encrypted message to be decrypted.
        :return: The decrypted message.
        :raises ValueError: If the shared key is not set.
        """
        if self.shared_key is None:
            raise ValueError("Shared key is not initialized.")
        
        # Decrypt by reapplying XOR (symmetric decryption)
        decrypted_message = self.encrypt_message(encrypted_message)  # XOR decryption
        print(f"Decrypted message: {decrypted_message}")  # Debugging line
        return decrypted_message

    def cleanup(self):
        """
        Clean up resources by deleting the quantum simulator.
        """
        print("Cleaning up simulator resources.")  # Debugging line
        del self.simulator