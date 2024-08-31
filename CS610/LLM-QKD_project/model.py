from transformers import pipeline

class GPT2Model:
    def __init__(self):
        self.model = pipeline('text-generation', model='gpt2')

    def generate_response(self, prompt):
        return self.model(prompt)[0]['generated_text']