from flask import Flask, request, jsonify
from datetime import timedelta
import os
import requests
import json
# from openai import OpenAI
from dotenv import load_dotenv
from flask_cors import CORS
import datetime
import pandas as pd

load_dotenv()
app = Flask(__name__)
CORS(app)
stocks_data = pd.read_csv('stocks.csv')

# gpt_client = OpenAI(base_url="https://api.groq.com/openai/v1", api_key=os.getenv("GROK_API_KEY"))

# For CORS
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response


@app.route('/api/stocks/autocomplete', methods=['GET'])
def autocomplete_stocks():
    query = request.args.get('q', '').lower()
    if not query:
        return jsonify([])  # Return an empty list if no query

    # Filter stocks containing the query
    filtered = stocks_data[
        stocks_data['Name'].str.contains(query, case=False, na=False) |
        stocks_data['Ticker'].str.contains(query, case=False, na=False)
    ]

    # Prepare the response
    results = filtered.head(5).to_dict(orient='records')  # Limit results to 5
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True, port=8000)
