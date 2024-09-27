import pytest
from flask import Flask
from unittest.mock import patch
from server import app, qkd, model

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_qkd_exchange(client):
    # Use the correct method name from QuantumProcessor
    with patch.object(qkd, 'generate_shared_key_server', return_value=None):
        response = client.post('/qkd', json={
            'alice_bits': ['1', '0', '0', '1', '1', '0', '0', '1', '1', '1'],
            'alice_bases': ['Z', 'X', 'Z', 'Z', 'X', 'Z', 'X', 'Z', 'Z', 'Z']
        })
        assert response.status_code == 200
        data = response.get_json()
        assert 'bob_bases' in data
        assert 'bob_results' in data

def test_generate_response(client):
    # First, initiate QKD to set the shared key
    with patch.object(qkd, 'generate_shared_key_server', return_value=None):
        client.post('/qkd', json={
            'alice_bits': ['1', '0', '0', '1', '1', '0', '0', '1', '1', '1'],
            'alice_bases': ['Z', 'X', 'Z', 'Z', 'X', 'Z', 'X', 'Z', 'Z', 'Z']
        })
    
    # Then, test the generate response endpoint
    response = client.post('/generate', json={
        'text': 'Encrypted message here', 
        'session_id': 'dummy_session_id'  # Provide a valid session_id
    })
    assert response.status_code == 200
    data = response.get_json()
    assert 'response' in data
