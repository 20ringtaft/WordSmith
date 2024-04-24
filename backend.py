from openai import OpenAI
import json 
from flask import Flask, request, jsonify, render_template

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
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        input_word = request.form.get('word')
        
        completion = client.chat.completions.create(
            model = "gpt-3.5-turbo",
            messages = [
                {"role": "system", "content": PROMPT},
                {"role": "user", "content": input_word}
            ]
        )
        
        synonym_sentence = completion.choices[0].message.content.split("\n")
        lines = [line.strip() for line in synonym_sentence if line.strip()]
        
        return render_template('index.html', lines=lines, input_word=input_word)
    
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)