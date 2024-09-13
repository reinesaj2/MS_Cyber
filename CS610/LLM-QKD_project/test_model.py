import pytest
from model import GPT2Model

@pytest.fixture
def gpt2_model():
    """Fixture to initialize the GPT2Model."""
    return GPT2Model()

def test_generate_response(gpt2_model):
    prompt = "Once upon a time"
    try:
        response = gpt2_model.generate_response(prompt)
        assert isinstance(response, str), "Response should be a string"
        assert len(response) > len(prompt), "Response should be longer than the prompt"
    except Exception as e:
        pytest.fail(f"Model failed to generate response: {e}")
