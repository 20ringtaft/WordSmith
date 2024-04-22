#This file serves as the main backend code for WordSmith, an online AI based service that provides synonyms and common uses of that word based on user input
from flask import Flask, request, jsonify
import chatgpt
import openai
import requests
key = "sk-proj-Yqhg7HAHkjEPly7Mcu6HT3BlbkFJ9OvC6SWxnZp3QCYlmaw3"