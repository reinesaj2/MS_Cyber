import pytest
from LLM_conduit import LLM_Conduit
from dataclasses import dataclass
from llm_pipeline_engine.models.llm_config import LLMConfig

@dataclass
class Query:
    prompt: str
    llm_config: LLMConfig = None

@pytest.fixture
def llm_conduit_instance():
    """Fixture to initialize the LLM_Conduit."""
    return LLM_Conduit()

@pytest.mark.asyncio
async def test_generate_response(llm_conduit_instance):
    prompt = "2+2=?"
    llm_config = LLMConfig(
        model='llama3.1:8b',  # Updated model identifier
        temperature=0.7,
        service='ollama',
        output_type='text'
    )
    query = Query(prompt=prompt, llm_config=llm_config)
    try:
        response = await llm_conduit_instance.generate(query)
        assert isinstance(response, str), "Response should be a string"
        assert len(response.strip()) > len(prompt), "Response should be longer than the prompt"
    except Exception as e:
        pytest.fail(f"Model failed to generate response: {e}")
