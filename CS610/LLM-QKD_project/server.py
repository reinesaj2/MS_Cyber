from flask import Flask, request, jsonify
from asgiref.wsgi import WsgiToAsgi
import warnings
import atexit
import numpy as np
import uuid  # Used for generating unique session identifiers

# Import the GPT2Model
from model import GPT2Model
from qkd import QuantumProcessor

warnings.filterwarnings(
    "ignore", category=FutureWarning, module="transformers.utils.generic"
)
warnings.filterwarnings(
    "ignore", category=FutureWarning, module="transformers.tokenization_utils_base"
)

app = Flask(__name__)

# Initialize server components
model = GPT2Model()
state_store = {}  # Stores state information for each session


@app.route("/qkd", methods=["POST"])
def qkd_exchange():
    print("\nStarting QKD Exchange.\n")
    data = request.json
    alice_bits = data.get("alice_bits")
    alice_bases = data.get("alice_bases")
    print(f"Received from Alice:\nBits: {alice_bits}\nBases: {alice_bases}\n")

    num_bits = len(alice_bits)
    qkd = QuantumProcessor(num_bits=num_bits)

    # Bob selects his measurement bases randomly
    bob_bases = ["Z" if np.random.rand() > 0.5 else "X" for _ in range(num_bits)]
    qkd.bob_bases = bob_bases
    print(f"Bob's random bases selection: {bob_bases}\n")

    # Prepare and measure qubits sent by Alice
    bob_results = []
    for i, (a_bit, a_basis, b_basis) in enumerate(
        zip(alice_bits, alice_bases, bob_bases)
    ):
        print(f"Processing qubit {i + 1}:")
        qc = qkd.prepare_qubit_state(a_bit, a_basis)
        print(
            f"    Prepared qubit state based on Alice's bit {a_bit} and basis '{a_basis}'."
        )
        measurement_result = qkd.measure_qubit_state(qc, b_basis)
        print(
            f"    Measured in Bob's basis '{b_basis}' and got result: {measurement_result}.\n"
        )
        bob_results.append(measurement_result)

    qkd.bob_results = bob_results

    # Generate a unique session ID and store Bob's data and qkd object
    session_id = str(uuid.uuid4())
    print(f"Generated session ID: {session_id}\n")
    state_store[session_id] = qkd  # Store the qkd instance for this session

    response = {
        "session_id": session_id,
        "bob_bases": bob_bases,
    }
    print(
        f"Sending response back to Alice with session ID: {session_id}, Bob's bases: {bob_bases}.\n"
    )
    return jsonify(response)


@app.route("/key_sifting", methods=["POST"])
def key_sifting():
    print("\nInitiating Key Sifting Process.\n")
    data = request.json
    session_id = data.get("session_id")
    matching_indices = data.get("matching_indices", [])
    print(f"Session ID received: {session_id}")
    print(f"Matching indices from Alice: {matching_indices}\n")

    # Retrieve qkd instance from the state store
    qkd = state_store.get(session_id)
    if not qkd:
        print(f"Invalid session ID received: {session_id}")
        return jsonify({"error": "Invalid session ID"}), 400

    qkd.generate_shared_key_server(matching_indices)
    print(
        f"Key sifting complete for session ID: {session_id}. Shared key established.\n"
    )
    return jsonify({"status": "Shared key generated on server"}), 200


@app.route("/generate", methods=["POST"])
def generate_response():
    print("\nMessage received. Decrypting and generating a response.\n")
    data = request.json
    encrypted_text = data.get("text")
    session_id = data.get("session_id")
    print(f"Session ID: {session_id}")
    print(f"Encrypted message received: {encrypted_text}\n")

    # Retrieve qkd instance from the state store
    qkd = state_store.get(session_id)
    if not qkd or qkd.shared_key is None:
        print(f"Shared key not initialized or invalid session ID: {session_id}")
        return jsonify({"error": "Shared key not initialized."}), 400

    try:
        decrypted_text = qkd.decrypt_message(encrypted_text)
        print(f"Decrypted message: {decrypted_text}\n")

        # Generate response using the model
        response_text = model.generate_response(decrypted_text)
        if response_text is None:
            print("Model failed to generate a response.")
            return jsonify({"error": "Model response generation failed"}), 500
        print(f"Model's response: {response_text}\n")

        encrypted_response = qkd.encrypt_message(response_text)
        print(f"Encrypted response being sent back to Alice: {encrypted_response}\n")
        return jsonify({"response": encrypted_response})
    except ValueError as e:
        print(f"Error during decryption for session ID {session_id}: {e}")
        return jsonify({"error": str(e)}), 400


def cleanup_resources():
    print("\nCleaning up resources.\n")
    model.cleanup()
    # No need to call qkd.cleanup() as it's per-session


atexit.register(cleanup_resources)

if __name__ == "__main__":
    print("Starting the Quantum Server.\n")
    asgi_app = WsgiToAsgi(app)
    import uvicorn

    uvicorn.run(asgi_app, host="0.0.0.0", port=5050)
