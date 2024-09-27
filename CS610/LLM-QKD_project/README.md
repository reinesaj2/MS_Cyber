# CS610 Project 1: Quantum Key Distribution (QKD) Encrypted Communication

## Project Overview

This project implements a secure client-server architecture utilizing Quantum Key Distribution (QKD) to encrypt communications between the client and server. The project demonstrates advanced cryptographic techniques by simulating QKD for secure message exchange.

## Files and Structure

- **server.py**: Hosts the server-side application using Flask and provides API endpoints for secure communication.
- **client.py**: A client script that simulates QKD, encrypts messages, sends them to the server, and decrypts the server's responses.
- **qkd.py**: Contains functions to simulate the QKD process and encrypt/decrypt messages using XOR.
- **requirements.txt**: Lists all Python dependencies required for the project.
- **README.md**: This document, providing an overview and instructions for the project.

## Setup Instructions

### 1. Clone the Repository

Ensure you have access to the `stu.cs.jmu.edu` server and clone the project files or upload them using Cyberduck.

### 2. Navigate to the Project Directory

```bash
cd Deliverable1-CS610
```

### 3. Set Up the Virtual Environment

The dependencies for this project require **Python 3.10**. If this Python version is not installed on the server and you don't have root access, you can use `pyenv` to install it locally in your home directory.

#### Option 1: Install `pyenv` Locally (Recommended)

This method allows you to install Python versions and manage virtual environments without root permissions.

##### Step 1: Clone `pyenv` Repository

```bash
git clone https://github.com/pyenv/pyenv.git ~/.pyenv
```

##### Step 2: Configure Your Shell

Add `pyenv` to your shell by adding these lines to your `~/.bashrc` or `~/.bash_profile`:

```bash
# Pyenv configuration
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init --path)"
eval "$(pyenv init -)"
```

Reload your shell configuration:

```bash
source ~/.bashrc
```

##### Step 3: Install Python 3.10 Using `pyenv`

Now, install Python **3.10.12**:

```bash
pyenv install 3.10.12
```

*Note*: If you encounter errors about missing build dependencies, you may need to install the required build tools locally or adjust to a Python version already available on the server.

##### Step 4: Set the Local Python Version for the Project

In the project directory:

```bash
cd Deliverable1-CS610
pyenv local 3.10.12
```

Verify the Python version:

```bash
python --version
```

This should output `Python 3.10.12`.

##### Step 5: Create and Activate the Virtual Environment with pyenv

```bash
pyenv virtualenv 3.10.12 QKD-LLM_env
pyenv activate QKD-LLM_env
```
Check if the virtual environment is activated and the Python version:

```bash
python --version
```

##### Step 6: Install Project Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

This ensures that all machines use the same Python version and dependencies, avoiding compatibility issues.

### 4. Run the Server

On the `stu.cs.jmu.edu` server, navigate to the project directory and run:

```bash
python path-to-server/server.py
```

### 5. SSH Tunneling and Accessing the Server

To securely access the server from your local machine, you can use SSH tunneling:

1. Open a new terminal and create an SSH tunnel:

    ```bash
    ssh -L 8000:134.126.141.221:8000 reinesaj@student.cs.jmu.edu
    ```

2. In a separate terminal (locally), use `curl` to send a POST request to the server.

    ```bash
    curl -X POST http://127.0.0.1:8000/qkd \
        -H "Content-Type: application/json" \
        -d '{"alice_bits": "101010", "alice_bases": "010101"}'
    ```

    ```bash
    curl -X POST http://127.0.0.1:8000/generate \
        -H "Content-Type: application/json" \
        -d '{"text": "Once upon a time"}'
    ```

    **Note**: Ensure you curl from a new terminal, not the same one you are SSH'd into.

### 6. Run the Client

On your local machine or another device:

```bash
python path-to-client/client.py
```

## How It Works

1. **QKD Simulation**: The `client.py` script simulates a Quantum Key Distribution (QKD) process to securely exchange a key with the server.
2. **Message Encryption**: The message is encrypted using XOR with the QKD key and sent to the server.
3. **Server Processing**: The server processes the encrypted message and sends an encrypted response back to the client.
4. **Decryption**: The client decrypts the server's response using the same QKD key.

## Known Issues

- There may be slight delays in processing due to encryption and decryption steps, as well as latency in the LLM.
- Ensure the SSH tunnel is active before running the client.
- Verify that the Python versions on both client and server match the required version to avoid compatibility issues.

## Conclusion

This project demonstrates the implementation of Quantum Key Distribution for secure communication in a client-server environment, showcasing the integration of modern cryptographic techniques.

## Contact

For any questions or issues, please reach out to Abraham J. Reines at reinesaj@dukes.jmu.edu.