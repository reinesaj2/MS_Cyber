import os
import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer
from flask import Flask, request, jsonify

app = Flask(__name__)

# Load the small GPT-2 model (as GPT-Neo is more resource-heavy)
model_name = "gpt2"
tokenizer = GPT2Tokenizer.from_pretrained(model_name)
model = GPT2LMHeadModel.from_pretrained(model_name)

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    input_text = data.get('text', '')
    
    inputs = tokenizer.encode(input_text, return_tensors='pt')
    outputs = model.generate(inputs, max_length=50, num_return_sequences=1)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    return jsonify({'response': response})

if __name__ == '__main__':
    # Run the server
    app.run(host='0.0.0.0', port=5000)