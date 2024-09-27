import requests
from qkd import QuantumProcessor


class QKDClient:
    def __init__(self, server_url="http://134.126.141.221:5050/qkd"):
        self.server_url = server_url
        print(f"Initializing QKDClient with server_url: {self.server_url}")
        self.qkd = QuantumProcessor()
        self.session_id = None  # Store session ID from the server
        print(f"QuantumProcessor initialized")
        print(f"Initial session_id: {self.session_id}")

    def initiate_qkd(self):
        self.qkd.num_bits = 4  # For example, set num_bits to 4
        self.qkd.generate_alice_bits_and_bases()
        alice_bits = self.qkd.alice_bits
        alice_bases = self.qkd.alice_bases
        print(f"Generated alice_bits: {alice_bits}")
        print(f"Generated alice_bases: {alice_bases}")

        try:
            payload = {"alice_bits": alice_bits, "alice_bases": alice_bases}
            print(f"Sending POST request to {self.server_url} with payload: {payload}")
            response = requests.post(
                self.server_url,
                json=payload,
            )
            print(f"Received response with status code: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"Response JSON data: {data}")
                self.session_id = data.get("session_id")
                print(f"Retrieved session_id: {self.session_id}")
                bob_bases = data.get("bob_bases")
                print(f"Retrieved bob_bases: {bob_bases}")

                matching_indices = self.qkd.generate_shared_key_client(
                    alice_bits, alice_bases, bob_bases
                )
                print(f"Matching indices: {matching_indices}")

                matching_data = {
                    "session_id": self.session_id,
                    "matching_indices": matching_indices,
                }
                print(f"Preparing matching_data for key sifting: {matching_data}")

                key_sifting_url = f"{self.server_url.replace('/qkd', '')}/key_sifting"
                print(
                    f"Sending POST request to {key_sifting_url} with matching_data: {matching_data}"
                )
                match_response = requests.post(
                    key_sifting_url,
                    json=matching_data,
                )
                print(f"Key Sifting response status code: {match_response.status_code}")
                if match_response.status_code != 200:
                    print(
                        f"Server returned an error during key sifting: {match_response.status_code}"
                    )
                else:
                    print("Key sifting completed successfully.")
            else:
                print(f"Server returned an error: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Error connecting to server: {e}")

    def send_encrypted_message(self, message):
        print(f"Preparing to send encrypted message: {message}")
        encrypted_message = self.qkd.encrypt_message(message)
        print(f"Encrypted message: {encrypted_message}")
        print(f"Session ID being used: {self.session_id}")

        try:
            generate_url = f"{self.server_url.replace('/qkd', '')}/generate"
            payload = {"text": encrypted_message, "session_id": self.session_id}
            print(f"Sending POST request to {generate_url} with payload: {payload}")
            response = requests.post(
                generate_url,
                json=payload,
            )
            print(f"Received response with status code: {response.status_code}")
            if response.status_code == 200:
                encrypted_response = response.json().get("response", "")
                print(f"Encrypted response from server: {encrypted_response}")
                decrypted_response = self.qkd.decrypt_message(encrypted_response)
                print(f"Decrypted response: {decrypted_response}")
                return decrypted_response
            else:
                print(f"Server returned an error: {response.status_code}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Error sending encrypted message: {e}")
            return None


if __name__ == "__main__":
    client = QKDClient()
    print("Initiating QKD process...")
    client.initiate_qkd()

    message = "What is the capital of France?"
    print(f"Sending message: {message}")
    decrypted_response = client.send_encrypted_message(message)
    print(f"Server Response: {decrypted_response}")
