from flask import Flask, request, jsonify
from model import GPT2Model
from qkd import QuantumProcessor

class QKDServer:
    def __init__(self):
        self.app = Flask(__name__)
        self.model = GPT2Model()
        self.qkd = QuantumProcessor()

        # Define routes
        self.app.add_url_rule('/qkd', 'qkd_exchange', self.qkd_exchange, methods=['POST'])
        self.app.add_url_rule('/generate', 'generate', self.generate_response, methods=['POST'])

    def qkd_exchange(self):
        data = request.json
        print(f"Received data: {data}")  # Debugging line
        alice_bits = data.get('alice_bits')
        alice_bases = data.get('alice_bases')
        # Simulate Bob's process
        bob_bases = 'BobBases'  # Replace with actual logic
        bob_results = 'BobResults'  # Replace with actual logic
        response = {'bob_bases': bob_bases, 'bob_results': bob_results}
        print(f"Response data: {response}")  # Debugging line
        return jsonify(response)

    def generate_response(self):
        data = request.json
        decrypted_text = data.get('text', '')  # Decrypt using shared key logic
        response_text = self.model.generate_response(decrypted_text)
        encrypted_response = response_text  # Encrypt using shared key logic
        return jsonify({'response': encrypted_response})

    def run(self):
        self.app.run(host='0.0.0.0', port=8000)

if __name__ == '__main__':
    server = QKDServer()
    server.app.run(host='0.0.0.0', port=8000, debug=True)
    
    # Curl the 'stu' server 
    # curl -X POST http://134.126.141.221:8000/generate -H "Content-Type: application/json" -d '{"text": "Once upon a time"}' --max-time 120