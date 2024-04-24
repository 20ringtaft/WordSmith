from openai import OpenAI
import json 
from flask import Flask, request, jsonify

app = Flask(__name__)

def read_json():
    with open("GPT.json","r") as f:
        config = json.load(f)
    return config

OPENAI_API_KEY = read_json().get("api_key")
PROMPT = read_json().get("prompt")
client = OpenAI(
    api_key=OPENAI_API_KEY
)
@app.route('/generate', methods=['POST'])
def generate():
    input = request.json.get('word')
    
    completion = client.chat.completions.create(
        model = "gpt-3.5-turbo",
        messages = [
            {"role": "system", "content": PROMPT},
            #replace "strong" with user input
            {"role": "user", "content": input}
        ]
    )
    # Extract and print synonyms and their sentences
    synonym_sentence = completion.choices[0].message.content.split("\n")
    lines = []
    for line in synonym_sentence:
        lines.append(line.strip())
    
    response = {
        "lines": lines
    }
    
    return jsonify(response)

if __name__ == "__main__":
    app.run(debug=True)