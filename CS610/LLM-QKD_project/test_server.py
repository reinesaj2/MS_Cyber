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
    with patch.object(qkd, 'generate_shared_key', return_value='10101010'):
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
    with patch.object(qkd, 'generate_shared_key', return_value='10101010'):
        client.post('/qkd', json={
            'alice_bits': ['1', '0', '0', '1', '1', '0', '0', '1', '1', '1'],
            'alice_bases': ['Z', 'X', 'Z', 'Z', 'X', 'Z', 'X', 'Z', 'Z', 'Z']
        })
    
    # Then, test the generate response endpoint
    response = client.post('/generate', json={'text': 'Nnbd!tpno!` uhld.//!'})
    assert response.status_code == 200
    data = response.get_json()
    assert 'response' in data
