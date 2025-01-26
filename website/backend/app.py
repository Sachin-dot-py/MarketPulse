from flask import Flask, request, jsonify
from datetime import timedelta
import os
import requests
import json
# from openai import OpenAI
from dotenv import load_dotenv
from flask_cors import CORS
import datetime

load_dotenv()
app = Flask(__name__)
CORS(app)

# gpt_client = OpenAI(base_url="https://api.groq.com/openai/v1", api_key=os.getenv("GROK_API_KEY"))

# For CORS
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response

# User registration
@app.route('/api/test', methods=['POST'])
def test():
    return "Hello, World!"


if __name__ == '__main__':
    app.run(debug=True, port=8000)
