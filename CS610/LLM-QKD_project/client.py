import requests
from qkd import QuantumProcessor

class QKDClient:
    def __init__(self, server_url='http://127.0.0.1:5000/qkd'):
        self.server_url = server_url
        self.shared_key = None
        self.qkd = QuantumProcessor()

    def initiate_qkd(self):
        self.qkd.prepare_quantum_state()
        alice_bits = self.qkd.measure_quantum_state()
        alice_bases = self.qkd.basis
        response = requests.post(self.server_url, json={'alice_bits': alice_bits, 'alice_bases': alice_bases})
        data = response.json()
        self.shared_key = self.qkd.generate_shared_key(alice_bits, alice_bases, data['bob_bases'], data['bob_results'])

    def encrypt_message(self, message):
        return ''.join(chr(ord(c) ^ int(self.shared_key[i % len(self.shared_key)], 2)) for i, c in enumerate(message))

    def send_encrypted_message(self, message):
        encrypted_message = self.encrypt_message(message)
        response = requests.post(f"{self.server_url.replace('/qkd', '')}/generate", json={'text': encrypted_message})
        encrypted_response = response.json().get('response', '')
        return self.encrypt_message(encrypted_response)

if __name__ == '__main__':
    client = QKDClient()
    client.initiate_qkd()
    
    message = "Hello, GPT-2!"
    decrypted_response = client.send_encrypted_message(message)
    print(f"Server Response: {decrypted_response}")