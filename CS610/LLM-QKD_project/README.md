# CS610 Project 1: QKD-Encrypted LLM for Secure Local Use

## Project Overview
This project implements a secure client-server architecture using a pre-trained language model (GPT-2) deployed on the `stu.cs.jmu.edu` server. The project demonstrates advanced cryptographic techniques by utilizing a Quantum Key Distribution (QKD) to encrypt communications between the client and server.

## Files and Structure
- **server.py**: Hosts the GPT-2 model using Flask and provides an API endpoint for text generation.
- **client.py**: A client script that simulates QKD, encrypts a message, sends it to the server, and decrypts the server's response.
- **qkd.py**: Contains functions to simulate the QKD process and encrypt/decrypt messages using XOR.
- **requirements.txt**: Lists all Python dependencies required for the project.
- **README.md**: This document, providing an overview and instructions for the project.

## Setup Instructions

### 1. Clone the Repository
Ensure you have access to the `stu.cs.jmu.edu` server and clone the project files or upload them using Cyberduck.

### 2, Navigate to Deliverable1-CS610
```bash
cd Deliverable1-CS610
```

### 3. Set Up the Virtual Environment
The dependencies for this project current require python3.10.12:
```bash
pip install python3.10.12 && python3.10 -m venv QKD-LLM_env && source QKD-LLM_env/bin/activate && pip install -r requirements.txt
```equirements.txt
```

### 4. Run the Server
On the `stu.cs.jmu.edu` server, navigate to the project directory and run:
```bash
python server.py
```

### 5. SSH Tunneling and Curling the Server
To securely access the server from your local machine, you can use SSH tunneling. Follow these steps:

1. Open a new terminal and create an SSH tunnel:
    ```bash
    ssh -L 8000:134.126.141.221:8000 reinesaj@student.cs.jmu.edu
    ```

2. In a third terminal (locally), use `curl` to send a POST request to the server:
    For establishing a secure key:
    ```bash
    curl -X POST http://127.0.0.1:8000/qkd \
        -H "Content-Type: application/json" \
        -d '{"alice_bits": "101010", "alice_bases": "010101"}'
    ```
    For generating LLM responses:
    ```bash
    curl -X POST http://127.0.0.1:8000/generate \
        -H "Content-Type: application/json" \
        -d '{"text": "Once upon a time"}'
    ```

    **Note**: Ensure you curl from a new terminal, not the same one you are SSH'd into.

### 6. Run the Client 
On your local machine or another device:
```bash
python LLM-QKD_project/client.py
```

## How It Works
1. **QKD Simulation**: The `client.py` script creates a Quantum Key Distribution (QKD) process to securely exchange a key with the server.
2. **Message Encryption**: The message is encrypted using XOR with the QKD key and sent to the server.
3. **Server Response**: The server processes the request using the GPT-2 model and sends an encrypted response back to the client.
4. **Decryption**: The client decrypts the server's response using the same QKD key.

## Known Issues
- There may be slight delays in processing due to encryption and decryption steps, as well as latency in the LLM.
- Ensure the SSH tunnel is active before running the client.

## Conclusion
This project demonstrates the integration of modern cryptographic techniques with machine learning, ensuring secure communication in a client-server environment.

## Contact
For any questions or issues, please reach out to Abraham J. Reines at reinesaj@dukes.jmu.edu.