import random

def generate_qkd_key(length=16):
    """Simulates a QKD process by generating a random key."""
    return ''.join(random.choice('01') for _ in range(length))

def xor_strings(s1, s2):
    """Encrypts/Decrypts using XOR and the QKD key."""
    return ''.join(chr(ord(a) ^ ord(b)) for a, b in zip(s1, s2))

def simulate_qkd_exchange():
    """Simulates a QKD exchange between two parties."""
    key = generate_qkd_key()
    print(f"Generated QKD Key: {key}")
    return key