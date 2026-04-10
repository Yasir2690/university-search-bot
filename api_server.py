from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import random
from datetime import datetime
import sqlite3

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load intents
with open('intents.json', 'r', encoding='utf-8') as f:
    intents = json.load(f)

# Simple response function
def get_response(user_input):
    user_lower = user_input.lower()
    
    for intent in intents['intents']:
        for pattern in intent['patterns']:
            if pattern.lower() in user_lower or user_lower in pattern.lower():
                return random.choice(intent['responses'])
    
    return "I can help with admissions, fees, courses, placements, hostel, sports, exams, and more!"

# API Routes
@app.route('/api/chat', methods=['POST'])
def chat():
    """Main chat endpoint"""
    data = request.json
    user_message = data.get('message', '')
    
    if not user_message:
        return jsonify({'error': 'Message is required'}), 400
    
    response = get_response(user_message)
    
    return jsonify({
        'response': response,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/intents', methods=['GET'])
def get_intents():
    """Get all available intents"""
    intent_list = [{'tag': i['tag'], 'patterns_count': len(i['patterns'])} for i in intents['intents']]
    return jsonify({'intents': intent_list})

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    })

@app.route('/api/faq', methods=['GET'])
def get_faq():
    """Get frequently asked questions"""
    faq = []
    for intent in intents['intents']:
        if intent['tag'] not in ['greeting', 'goodbye']:
            faq.append({
                'category': intent['tag'].replace('_', ' ').title(),
                'example_question': intent['patterns'][0],
                'sample_answer': intent['responses'][0]
            })
    return jsonify({'faq': faq})

if __name__ == '__main__':
    print("🚀 API Server starting...")
    print("📍 Available endpoints:")
    print("   POST http://localhost:5000/api/chat")
    print("   GET  http://localhost:5000/api/intents")
    print("   GET  http://localhost:5000/api/faq")
    print("   GET  http://localhost:5000/api/health")
    print("\nPress Ctrl+C to stop")
    app.run(debug=True, host='0.0.0.0', port=5000)