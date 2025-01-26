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
from anthropic import AnthropicBedrock
import csv


load_dotenv()
app = Flask(__name__)
CORS(app)
stocks_data = pd.read_csv('stocks.csv')

client = AnthropicBedrock(
    aws_access_key=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    aws_session_token=os.getenv("AWS_SESSION_TOKEN"),  # Optional if using temporary credentials
    aws_region=os.getenv("AWS_DEFAULT_REGION", "us-west-2"),  # Default to "us-west-2" if not set
)

# Define the model to use (e.g., Amazon Titan)
model_name = "anthropic.claude-3-5-haiku-20241022-v1:0"

def summarise_news(headline, full_text):

    # Prepare the prompt
    prompt = f"""
    You are an advanced financial text summarization AI. Your task is to generate a concise upto 3-line summary of the important financial content from a given article. Only include key points about the article’s financial context, metrics, or events. Return only the summary—no markdown, no explanations, preamble, or additional text. Follow the format of the examples below.

    Examples:

    Input:
    {{
    "headline": "Tech Giant Posts Record Q4 Earnings",
    "full_text": "Tech Giant Inc. reported record earnings for Q4 2024, with a net income of $2.5 billion, up 15% year-over-year. Revenue grew by 10% to $15 billion, driven by strong performance in its cloud services division. The company also announced a $1 billion stock buyback program."
    }}

    Output:
    Tech Giant Inc. reported $2.5 billion in Q4 2024 net income, a 15% increase year-over-year. Revenue rose 10% to $15 billion, led by growth in cloud services. The company plans a $1 billion stock buyback.

    Input:
    {{
    "headline": "Auto Manufacturer Expands EV Production",
    "full_text": "Auto Manufacturer Ltd. announced plans to increase its electric vehicle production capacity by 50% over the next three years. The company aims to invest $3 billion in new facilities and expects this move to boost its market share in the EV sector. Analysts predict a significant rise in the company's EV sales by 2027."
    }}

    Output:
    Auto Manufacturer Ltd. plans to expand EV production capacity by 50% in three years, investing $3 billion in new facilities. The move aims to grow market share in the EV sector. Analysts expect higher EV sales by 2027.


    Input:
    {{
    "headline": "{headline}",
    "full_text": "{full_text}"
    }}

    Output:
    """

    message = client.messages.create(
        model=model_name,
        max_tokens=256,
        messages=[{"role": "user", "content": prompt}]
    )

    # Extract and return the summary from the response
    return message.content[0].text


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

@app.route('/api/get_events', methods=['GET'])
def get_events():
    data = []
    # Read the CSV file
    df = pd.read_csv("analysis.csv")

    # Convert comma-separated strings back to lists
    df['tickers'] = df['tickers'].apply(lambda x: x.split(","))
    df['percentpricechanges'] = df['percentpricechanges'].apply(lambda x: list(map(float, x.split(","))))

    
    # Generate summaries and price change mappings
    df['summary'] = df.apply(lambda row: summarise_news(row['headline'], row['text']), axis=1)
    df['pricechanges'] = df.apply(lambda row: dict(zip(row['tickers'], row['percentpricechanges'])), axis=1)

    # Select required columns for the final output
    processed_data = df[['headline', 'summary', 'pricechanges']]
    # Convert the DataFrame to a list of dictionaries (if needed)
    data = processed_data.to_dict(orient='records')
    
    # Return JSON response
    return jsonify(data), 200

if __name__ == '__main__':
    app.run(debug=True, port=8000)
