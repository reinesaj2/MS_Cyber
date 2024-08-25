import requests
from qkd import simulate_qkd_exchange, xor_strings

server_url = 'http://stu.cs.jmu.edu:5000/generate'

def main():
    # Simulate QKD key exchange
    qkd_key = simulate_qkd_exchange()

    # Encrypt the message using XOR with QKD key
    message = "Hello, GPT-2!"
    encrypted_message = xor_strings(message, qkd_key)

    # Send the encrypted message to the server
    response = requests.post(server_url, json={'text': encrypted_message})
    encrypted_response = response.json().get('response', '')

    # Decrypt the server's response
    decrypted_response = xor_strings(encrypted_response, qkd_key)
    print(f"Server Response: {decrypted_response}")

if __name__ == '__main__':
    main()