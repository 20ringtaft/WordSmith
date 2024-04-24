import requests
import json

url = 'http://127.0.0.1:5000/generate'

# Define the word for which you want to generate synonyms
data = {
    'word': 'strong'
}

# Send a POST request to the Flask app
response = requests.post(url, json=data)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Print the response JSON
    print(response.json())
else:
    # Print an error message if the request failed
    print('Error:', response.text)