#This file serves as the main backend code for WordSmith, an online AI based service that provides synonyms and common uses of that word based on user input
from flask import Flask, request, jsonify
import chatgpt
from openai import OpenAI
import requests
import json
app = Flask(__name__)

def get_config():
    with open("GPT.json","r") as f:
        config = json.load(f)
    return config

config = get_config()
api_secret_key = config.get("api_key")
OPENAI_API_URL = "https://api.openai.com/v1/completions"

def generate_synonyms(word, api_key, num_synonyms=5, sentence_count=2):
    try:
        synonyms = chatgpt.get_synonyms(word, api_key=api_key, num_synonyms=num_synonyms)
        synonym_sentences = {}
        for synonym in synonyms:
            prompt = f"Provide {sentence_count} sentences demonstrating the use of the word '{synonym}'."
            response = generate_completion(prompt, api_key)
            sentences = response.strip().split('\n')[:sentence_count]
            synonym_sentences[synonym] = sentences
        return {"synonyms":synonyms, "sentences":synonym_sentences}
    except Exception as e:
        raise Exception(f"Error generating synonyms: {str(e)}")


def generate_completion(prompt, api_key):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    data = {
        "model": "text-davinci-002",
        "prompt":prompt,
        "max_tokens": 100,
        "temperature": 0.7
    }
    response = requests.post(OPENAI_API_URL, headers=headers, json=data)
    response_data = response.json()
    if response.status_code == 200:
        print("success")
        return response_data["choices"][0]["text"]
    else:
        raise Exception(f"Error generating completion: {response_data.get('error', {}).get('message', 'Unknown error')}")
    
@app.route('/generate_synonym', methods=['POST'])
def handle_generate_synonyms():
    data = request.get_json()
    word = data.get('word')
    if not word: 
        return jsonify({"error": "Word not provided"}), 400
    
    try: 
        synonyms_data = generate_synonyms(word, api_secret_key)
        print("Synonyms data:", synonyms_data)
        print("cheeseburger")
        return jsonify(synonyms_data),200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)