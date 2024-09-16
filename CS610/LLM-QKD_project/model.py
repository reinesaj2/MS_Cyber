from transformers import pipeline
import gc


class GPT2Model:
    """
    GPT2Model is responsible for generating text responses using the GPT-2 model.
    It initializes the model, generates responses based on a given prompt, and cleans up resources.
    """

    def __init__(self):
        """
        Initialize the GPT2Model with the GPT-2 text generation pipeline.
        The model is set to use the CPU.
        """
        self.model = pipeline(
            "text-generation", model="gpt2", device=-1
        )  # Set device to CPU

    def generate_response(
        self, prompt, max_length=50, num_return_sequences=1, temperature=1.0
    ):
        """
        Generate a text response based on the given prompt.

        :param prompt: The input text prompt for the model.
        :param max_length: The maximum length of the generated text.
        :param num_return_sequences: The number of generated sequences to return.
        :param temperature: The sampling temperature for text generation.
        :return: The generated text response.
        """
        try:
            return self.model(
                prompt,
                max_length=max_length,
                num_return_sequences=num_return_sequences,
                temperature=temperature,
                pad_token_id=self.model.tokenizer.eos_token_id,
                clean_up_tokenization_spaces=True,
            )[0]["generated_text"]
        except Exception as e:
            print(f"An error occurred during text generation: {e}")
            return ""

    def cleanup(self):
        """
        Clean up resources by deleting the model and performing garbage collection.
        """
        del self.model
        gc.collect()


if __name__ == "__main__":
    gpt2 = GPT2Model()
    prompt = "Once upon a time"
    response = gpt2.generate_response(prompt)
    print(response)
    gpt2.cleanup()
