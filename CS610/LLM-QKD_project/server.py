import os

os.environ["TOKENIZERS_PARALLELISM"] = "false"  # Disable tokenizers parallelism

from flask import Flask, request, jsonify
from asgiref.wsgi import WsgiToAsgi
import warnings
import atexit
import numpy as np

from model import GPT2Model
from qkd import QuantumProcessor

# Suppress the FutureWarning
warnings.filterwarnings(
    "ignore", category=FutureWarning, module="transformers.tokenization_utils_base"
)

app = Flask(__name__)  # Expose app at the module level

# Instantiate your server components at the module level
model = GPT2Model()
qkd = QuantumProcessor()


@app.route("/qkd", methods=["POST"])
def qkd_exchange():
    data = request.json
    print(f"Received data: {data}")  # Debugging line
    alice_bits = data.get("alice_bits")
    alice_bases = data.get("alice_bases")

    # Simulate Bob's process
    bob_bases = ["Z" if np.random.rand() > 0.5 else "X" for _ in alice_bits]
    bob_results = [
        qkd.measure_quantum_state(qkd.prepare_quantum_state(bit, basis), basis)
        for bit, basis in zip(alice_bits, bob_bases)
    ]

    qkd.shared_key = qkd.generate_shared_key(
        alice_bits, alice_bases, bob_bases, bob_results
    )
    print(f"Shared key set: {qkd.shared_key}")  # Debugging line
    response = {"bob_bases": bob_bases, "bob_results": bob_results}
    print(f"Response data: {response}")  # Debugging line
    return jsonify(response)


@app.route("/generate", methods=["POST"])
def generate_response():
    data = request.json
    encrypted_text = data.get("text", "")
    print(f"Encrypted text received: {encrypted_text}")  # Debugging line
    print(f"Shared key before decryption: {qkd.shared_key}")  # Debugging line
    decrypted_text = qkd.decrypt_message(
        encrypted_text
    )  # Decrypt using shared key logic
    print(f"Decrypted text: {decrypted_text}")  # Debugging line
    if decrypted_text is None:
        return jsonify({"error": "Decryption failed"}), 400
    response_text = model.generate_response(decrypted_text)
    print(f"Response text: {response_text}")  # Debugging line
    if response_text is None:
        return jsonify({"error": "Model response generation failed"}), 500
    encrypted_response = qkd.encrypt_message(
        response_text
    )  # Encrypt using shared key logic
    print(f"Encrypted response: {encrypted_response}")  # Debugging line
    return jsonify({"response": encrypted_response})


def cleanup_resources():
    model.cleanup()
    qkd.cleanup()


atexit.register(cleanup_resources)

if __name__ == "__main__":
    asgi_app = WsgiToAsgi(app)
    import uvicorn

    uvicorn.run(asgi_app, host="0.0.0.0", port=8000)
