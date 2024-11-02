from flask import Flask, request, jsonify 
from flask_cors import CORS
from invoke_llm import capture_parameter_using_llm
import openai
import pandas as pd

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}}, supports_credentials=True)

# Load the Excel data once when the app starts
excel_file_path = 'Hyderabad_Ct_scrapedData.xlsx'
car_data = pd.read_excel(excel_file_path)

@app.route('/api/get_chatbot_response', methods=['POST'])
def get_chatbot_response():
    data = request.get_json()
    message = data.get('message')
    response_message = capture_parameter_using_llm(message)
    return jsonify({'message': response_message})

if __name__ == '__main__':
    app.run(debug=True)