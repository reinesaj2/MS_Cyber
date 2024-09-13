import requests
from qkd import QuantumProcessor

class QKDClient:
    def __init__(self, server_url='http://localhost:8000/qkd'):
        self.server_url = server_url
        self.shared_key = None
        self.qkd = QuantumProcessor()
        print("QKDClient initialized with server URL:", self.server_url)

    def initiate_qkd(self):
        print("Preparing quantum state...")
        self.qkd.prepare_quantum_state()
        alice_bits = self.qkd.measure_quantum_state()
        alice_bases = self.qkd.basis
        print("Sending QKD initiation request to server...")
        response = requests.post(self.server_url, json={'alice_bits': alice_bits, 'alice_bases': alice_bases})
        print(f"Server response content: {response.content}")  # Debugging line
        data = response.json()
        print("Generating shared key...")
        self.shared_key = self.qkd.generate_shared_key(alice_bits, alice_bases, data['bob_bases'], data['bob_results'])
        print("Shared key generated:", self.shared_key)

    def encrypt_message(self, message):
        print("Encrypting message...")
        encrypted_message = ''.join(chr(ord(c) ^ int(self.shared_key[i % len(self.shared_key)], 2)) for i, c in enumerate(message))
        print("Message encrypted.")
        return encrypted_message

    def send_encrypted_message(self, message):
        print("Sending encrypted message to server...")
        encrypted_message = self.encrypt_message(message)
        try:
            response = requests.post(f"{self.server_url.replace('/qkd', '')}/generate", json={'text': encrypted_message})
            print(f"Raw server response: {response.content}")  # Debugging line
            encrypted_response = response.json().get('response', '')
            return self.qkd.decrypt_message(encrypted_response)  # Decrypt the response
        except requests.exceptions.RequestException as e:
            print(f"Error sending encrypted message: {e}")
            return None
        
if __name__ == '__main__':
    client = QKDClient()
    client.initiate_qkd()
    
    message = "Once upon a time... "
    print("Sending message:", message)
    decrypted_response = client.send_encrypted_message(message)
    print(f"Server Response: {decrypted_response}")