import os
import re
import json
from google.genai import Client

# Initialize the client with the GEMINI_API_KEY
client = Client(api_key=os.getenv('GEMINI_API_KEY'))

def generate_content_with_gemini(prompt):
    try:
        # Call the model
        response = client.models.generate_content(model_name='gemini-1.5-flash', prompt=prompt)
        
        # Parsing the response
        raw_response = response.text
        json_data = extract_json(raw_response)
        return json_data
    except Exception as e:
        raise ValueError(f"Error during content generation: {e}. Raw response: {raw_response}")

def extract_json(raw_response):
    # Remove JSON fences
    json_without_fences = raw_response.replace('```json', '').replace('```', '').strip()
    # Regex to find the first JSON array
    match = re.search(r'\[.*?\]', json_without_fences)
    if match:
        return json.loads(match.group(0))
    else:
        raise ValueError("No valid JSON array found in the response.")

# Example usage
# content = generate_content_with_gemini('Some prompt string')
