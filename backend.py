#This file serves as the main backend code for WordSmith, an online AI based service that provides synonyms and common uses of that word based on user input
from flask import Flask, request, jsonify
import chatgpt
import openai
import requests
import json

def get_api_key():
    with open("GPT.json","r") as f:
        config = json.load(f)
    return config.get("api_key")

api_key = get_api_key()

