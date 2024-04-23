from openai import OpenAI
import requests
import json

def get_config():
    with open("GPT.json","r") as f:
        config = json.load(f)
    return config

def generate_synonyms(word, api_key, num_synonyms=5, sentence_count=2):
    prompt = get_config().get("prompt")
    try:
        response = generate_completion(prompt, api_key)
        synonyms = response.strip().split('\n')[:num_synonyms]
        return synonyms
    except Exception as e:
        raise Exception(f"Error generating synonyms: {str(e)}")

def generate_completion(prompt, api_key):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    data = {
        "model": "gpt-3.5-turbo",
        "prompt": prompt
    }
    response = requests.post(OPENAI_API_URL, headers=headers, json=data)
    response_data = response.json()
    if response.status_code == 200:
        return response_data["choices"][0]["text"]
    else:
        raise Exception(f"Error generating completion: {response_data.get('error', {}).get('message', 'Unknown error')}")

def test_generate_synonyms():
    word = "happy"
    api_key = get_config().get("api_key")
    try:
        synonyms = generate_synonyms(word, api_key)
        print("Synonyms:", synonyms)
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
    test_generate_synonyms()