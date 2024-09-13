from transformers import pipeline
import gc

class GPT2Model:
    def __init__(self):
        self.model = pipeline("text-generation", model="gpt2", device=-1)  # Set device to CPU

    def generate_response(self, prompt, max_length=50, num_return_sequences=1, temperature=1.0):
        try:
            return self.model(
                prompt,
                max_length=max_length,
                num_return_sequences=num_return_sequences,
                temperature=temperature,
                pad_token_id=self.model.tokenizer.eos_token_id,
                clean_up_tokenization_spaces=True
            )[0]["generated_text"]
        except Exception as e:
            print(f"An error occurred during text generation: {e}")
            return ""
    
    def cleanup(self):
        del self.model
        gc.collect()
        
if __name__ == "__main__":
    gpt2 = GPT2Model()
    prompt = "Once upon a time"
    response = gpt2.generate_response(prompt)
    print(response)
    gpt2.cleanup()