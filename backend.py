#This file serves as the main backend code for WordSmith, an online AI based service that provides synonyms and common uses of that word based on user input
from flask import Flask, request, jsonify
import chatgpt
import openai

