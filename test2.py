from openai import OpenAI
import json 

def read_json():
    with open("GPT.json","r") as f:
        config = json.load(f)
    return config

OPENAI_API_KEY = read_json().get("api_key")
PROMPT = read_json().get("prompt")
client = OpenAI(
    api_key=OPENAI_API_KEY
)
completion = client.chat.completions.create(
    model = "gpt-3.5-turbo",
    messages = [
        {"role": "system", "content": PROMPT},
        #replace "strong" with user input
        {"role": "user", "content": "strong"}
    ]
)


# Extract and print synonyms and their sentences
print(completion.choices[0].message)
sentence = completion.choices[0].message.content.split("\n")
for line in sentence:
    print(line)