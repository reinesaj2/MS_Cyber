import requests
from qkd import QuantumProcessor


class QKDClient:
    """
    QKDClient is responsible for initiating the Quantum Key Distribution (QKD) process with the server,
    encrypting messages using the shared key, and sending encrypted messages to the server.
    """

    def __init__(self, server_url="http://0.0.0.0:8000/qkd"):
        """
        Initialize the QKDClient with the server URL and create an instance of QuantumProcessor.

        :param server_url: The URL of the server to initiate QKD with.
        """
        self.server_url = server_url
        self.shared_key = None
        self.qkd = QuantumProcessor()
        print("QKDClient initialized with server URL:", self.server_url)

    def initiate_qkd(self):
        """
        Initiate the QKD process by preparing the quantum state, measuring it, and sending the results to the server.
        The server responds with its own measurement results, which are used to generate a shared key.
        """
        print("Preparing quantum state...")
        alice_bits = ['0', '1', '0', '1']  # Example bits
        alice_bases = ['Z', 'X', 'Z', 'X']  # Example bases

        for bit, basis in zip(alice_bits, alice_bases):
            self.qkd.prepare_quantum_state(bit, basis)
        
        alice_measurements = [self.qkd.measure_quantum_state(self.qkd.prepare_quantum_state(bit, basis), basis) for bit, basis in zip(alice_bits, alice_bases)]
        print("Sending QKD initiation request to server...")
        try:
            response = requests.post(
                self.server_url,
                json={"alice_bits": alice_bits, "alice_bases": alice_bases},
            )
            print(f"Server response content: {response.content}")  # Debugging line

            if response.status_code == 200:
                try:
                    data = response.json()
                    print("Generating shared key...")
                    self.shared_key = self.qkd.generate_shared_key(
                        alice_bits, alice_bases, data["bob_bases"], data["bob_results"]
                    )
                    print("Shared key generated:", self.shared_key)
                except requests.exceptions.JSONDecodeError as e:
                    print(f"Error decoding JSON response: {e}")
            else:
                print(f"Server returned an error: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Error connecting to server: {e}")

    def encrypt_message(self, message):
        """
        Encrypt a message using the shared key.

        :param message: The plaintext message to be encrypted.
        :return: The encrypted message, or None if the shared key is not initialized.
        """
        if self.shared_key is None:
            print("Error: Shared key is not initialized.")
            return None

        print("Encrypting message...")
        encrypted_message = "".join(
            chr(ord(c) ^ int(self.shared_key[i % len(self.shared_key)], 2))
            for i, c in enumerate(message)
        )
        print("Message encrypted.")
        return encrypted_message

    def send_encrypted_message(self, message):
        """
        Send an encrypted message to the server and decrypt the server's response.

        :param message: The plaintext message to be encrypted and sent.
        :return: The decrypted response from the server, or None if an error occurs.
        """
        print("Sending encrypted message to server...")
        encrypted_message = self.encrypt_message(message)
        if encrypted_message is None:
            print(
                "Error: Could not encrypt message because the shared key is not initialized."
            )
            return None

        try:
            response = requests.post(
                f"{self.server_url.replace('/qkd', '')}/generate",
                json={"text": encrypted_message},
            )
            print(f"Raw server response: {response.content}")  # Debugging line
            encrypted_response = response.json().get("response", "")
            return self.qkd.decrypt_message(encrypted_response)  # Decrypt the response
        except requests.exceptions.RequestException as e:
            print(f"Error sending encrypted message: {e}")
            return None


if __name__ == "__main__":
    client = QKDClient()
    client.initiate_qkd()

    message = "Once upon a time... "
    print("Sending message:", message)
    decrypted_response = client.send_encrypted_message(message)
    print(f"Server Response: {decrypted_response}")
