from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
import numpy as np


class QuantumChannel:
    """
    Represents the quantum channel through which qubits are transmitted.
    """

    def __init__(self):
        self.simulator = AerSimulator()
        print("QuantumChannel initialized.")

    def transmit(self, qubits):
        """
        Simulates the transmission of qubits through the quantum channel.
        :param qubits: List of QuantumCircuit objects representing the qubits.
        :return: List of QuantumCircuit objects after transmission.
        """
        # In a real scenario, the channel might introduce noise or loss.
        # For simulation purposes, we'll assume an ideal channel.
        print("Qubits transmitted through quantum channel.")
        return qubits


class Alice:
    """
    Represents Alice in the BB84 protocol.
    """

    def __init__(self, num_bits=100):
        self.num_bits = num_bits
        self.bits = None
        self.bases = None
        self.qubits = None
        self.shared_key = None  # Added shared_key attribute
        print("Alice initialized.")

    def generate_bits_and_bases(self):
        """
        Generate random bits and bases for Alice.
        """
        self.bits = np.random.randint(2, size=self.num_bits).tolist()
        self.bases = np.random.choice(["Z", "X"], size=self.num_bits).tolist()
        print("Alice's bits and bases generated.")

    def prepare_qubits(self):
        """
        Prepare qubits based on Alice's bits and bases.
        """
        self.qubits = []
        for bit, basis in zip(self.bits, self.bases):
            qc = QuantumCircuit(1, 1)
            if bit == 1:
                qc.x(0)
            if basis == "X":
                qc.h(0)
            self.qubits.append(qc)
        print("Alice's qubits prepared.")

    def prepare_qubit_state(self, bit, basis):
        """
        Prepare a single qubit based on the bit and basis.
        """
        qc = QuantumCircuit(1, 1)
        if bit == 1:
            qc.x(0)
        if basis == "X":
            qc.h(0)
        return qc

    def encrypt_message(self, message):
        """
        Encrypt a message using the shared key.
        """
        if self.shared_key is None:
            raise ValueError("Shared key not established.")
        key_stream = "".join(map(str, self.shared_key))
        key_repeated = (key_stream * (len(message) // len(key_stream) + 1))[
            : len(message)
        ]
        encrypted = "".join(chr(ord(c) ^ ord(k)) for c, k in zip(message, key_repeated))
        return encrypted

    def decrypt_message(self, encrypted_message):
        """
        Decrypt a message using the shared key.
        """
        return self.encrypt_message(encrypted_message)  # Symmetric encryption


class Bob:
    """
    Represents Bob in the BB84 protocol.
    """

    def __init__(self, num_bits=100):
        self.num_bits = num_bits
        self.bases = None
        self.results = None
        self.shared_key = None  # Added shared_key attribute
        self.simulator = AerSimulator()
        print("Bob initialized.")

    def generate_bases(self):
        """
        Generate random bases for Bob.
        """
        self.bases = np.random.choice(["Z", "X"], size=self.num_bits).tolist()
        print("Bob's bases generated.")

    def measure_qubit_state(self, qc, basis):
        """
        Measure a single qubit in the given basis.
        """
        measurement_qc = qc.copy()
        if basis == "X":
            measurement_qc.h(0)
        measurement_qc.measure(0, 0)
        job = self.simulator.run(measurement_qc, shots=1)
        result = job.result()
        counts = result.get_counts()
        bit = int(list(counts.keys())[0])
        return bit

    def encrypt_message(self, message):
        """
        Encrypt a message using the shared key.
        """
        if self.shared_key is None:
            raise ValueError("Shared key not established.")
        key_stream = "".join(map(str, self.shared_key))
        key_repeated = (key_stream * (len(message) // len(key_stream) + 1))[
            : len(message)
        ]
        encrypted = "".join(chr(ord(c) ^ ord(k)) for c, k in zip(message, key_repeated))
        return encrypted

    def decrypt_message(self, encrypted_message):
        """
        Decrypt a message using the shared key.
        """
        return self.encrypt_message(encrypted_message)  # Symmetric encryption


class KeySifter:
    """
    Handles key sifting between Alice and Bob.
    """

    @staticmethod
    def sift_keys(alice_bases, bob_bases, alice_bits, bob_results):
        """
        Sift the keys by comparing Alice's and Bob's bases.
        :return: Sifted keys and indices of matching bases.
        """
        matching_indices = []
        sifted_key_alice = []
        sifted_key_bob = []
        for i, (a_basis, b_basis) in enumerate(zip(alice_bases, bob_bases)):
            if a_basis == b_basis:
                matching_indices.append(i)
                sifted_key_alice.append(alice_bits[i])
                sifted_key_bob.append(bob_results[i])
        print(f"Keys sifted. {len(sifted_key_alice)} bits remain after sifting.")
        return sifted_key_alice, sifted_key_bob, matching_indices


class QuantumProcessor:
    """
    Handles the QKD operations for both client and server.
    """

    def __init__(self, num_bits=100):
        self.num_bits = num_bits
        self.simulator = AerSimulator()

        self.alice_bits = None
        self.alice_bases = None
        self.bob_bases = None
        self.bob_results = None
        self.shared_key = None

    def generate_alice_bits_and_bases(self):
        """
        Generates random bits and bases for Alice.
        """
        self.alice_bits = np.random.randint(2, size=self.num_bits).tolist()
        self.alice_bases = np.random.choice(["Z", "X"], size=self.num_bits).tolist()

    def prepare_qubit_state(self, bit, basis):
        """
        Prepare a single qubit based on the bit and basis.
        """
        qc = QuantumCircuit(1, 1)
        if bit == 1:
            qc.x(0)
        if basis == "X":
            qc.h(0)
        return qc

    def measure_qubit_state(self, qc, basis):
        """
        Measure a single qubit in the given basis.
        """
        measurement_qc = qc.copy()
        if basis == "X":
            measurement_qc.h(0)
        measurement_qc.measure(0, 0)
        job = self.simulator.run(measurement_qc, shots=1)
        result = job.result()
        counts = result.get_counts()
        bit = int(list(counts.keys())[0])
        return bit

    def generate_shared_key_server(self, matching_indices):
        """
        Generates the shared key on the server side using matching indices.
        """
        if self.bob_results is None or self.bob_bases is None:
            raise ValueError("Bob's results or bases not initialized.")
        self.shared_key = [self.bob_results[i] for i in matching_indices]

    def generate_shared_key_client(self, alice_bits, alice_bases, bob_bases):
        """
        Generates the shared key on the client side and returns matching indices.
        """
        matching_indices = []
        self.shared_key = []
        for i, (a_basis, b_basis) in enumerate(zip(alice_bases, bob_bases)):
            if a_basis == b_basis:
                matching_indices.append(i)
                self.shared_key.append(alice_bits[i])
        return matching_indices

    def encrypt_message(self, message):
        """
        Encrypt a message using the shared key.
        """
        if self.shared_key is None:
            raise ValueError("Shared key not established.")
        key_stream = "".join(map(str, self.shared_key))
        key_repeated = (key_stream * (len(message) // len(key_stream) + 1))[
            : len(message)
        ]
        encrypted = "".join(chr(ord(c) ^ ord(k)) for c, k in zip(message, key_repeated))
        return encrypted

    def decrypt_message(self, encrypted_message):
        """
        Decrypt a message using the shared key.
        """
        return self.encrypt_message(encrypted_message)  # Symmetric encryption

    def gaussian_modulation(self):
        """
        Returns a random bit (0 or 1).
        """
        return np.random.randint(0, 2)
