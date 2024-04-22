#This file serves as the main backend code for WordSmith, an online AI based service that provides synonyms and common uses of that word based on user input
from flask import Flask, request, jsonify
import chatgpt
import OpenAI
import requests
import json

def get_config():
    with open("GPT.json","r") as f:
        config = json.load(f)
    return config

app = Flask(__name__)
config = get_config()
api_secret_key = config.get("api_key")

client = OpenAI(
    organization = 'org-H8vsA8rqAe7U6UqVTjAuPNc1',
    project  = 'proj_zG0xupI6uNXhOsyFNVL9jhv8',
)

@app.route('/generate_synonym', methods=['POST'])
def generate_synonyms():
    data = request.get_json()
    word = data.get('word')
    if not word: 
        return jsonify({"error": "Word not provided"}), 400
    
    try: 
        syn_count = config.get("syn_count", 5)
        sentence_count = config.get("sentence_count", 2)
        
        synonyms = chatgpt.get_synonyms(word, api_key = api_secret_key, num_synonyms = syn_count)
        synonym_sentences = {}
        for synonym in synonyms: 
            prompt = f"Provide {sentence_count} sentences demonstrating the use of the word '{synonym}'."
            completion = client.complete(prompt, api_key = api_secret_key, max_tokens = 100)
            sentences = completion.choices[0].text.strip().split('\n')[:sentence_count]
            synonym_sentences[synonym] = sentences

        return jsonify({"synonyms": synonyms, "sentences": synonym_sentences}), 200
    except Exception as e:
        return jsonify({"error": str(e)}),500 