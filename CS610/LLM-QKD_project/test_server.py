import pytest
from flask import Flask
from server import QKDServer

@pytest.fixture
def client():
    server = QKDServer()
    server.app.config['TESTING'] = True
    with server.app.test_client() as client:
        yield client

def test_qkd_exchange(client):
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
    client.post('/qkd', json={
        'alice_bits': ['1', '0', '0', '1', '1', '0', '0', '1', '1', '1'],
        'alice_bases': ['Z', 'X', 'Z', 'Z', 'X', 'Z', 'X', 'Z', 'Z', 'Z']
    })
    
    # Then, test the generate response endpoint
    response = client.post('/generate', json={'text': 'Nnbd!tpno!` uhld.//!'})
    assert response.status_code == 200
    data = response.get_json()
    assert 'response' in data
