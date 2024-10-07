
from flask import Flask, request, jsonify
import requests
import nltk
from nltk.tokenize import word_tokenize

# Download NLTK data
nltk.download('punkt')
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Initialize SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phone_number = db.Column(db.String(15), unique=True, nullable=False)

# Create the database
with app.app_context():
    db.create_all()

@app.route('/subscribe', methods=['POST'])
def subscribe():
    phone_number = request.json.get('phone_number')
    if not phone_number:
        return jsonify({"error": "Phone number is required"}), 400

    user = User(phone_number=phone_number)
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "Subscription successful"}), 201

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    tokens = word_tokenize(user_message)
    response_message = "Processed response"  # Replace with actual NLP logic
    send_sms('YOUR_API_KEY', response_message, '+18005550199', '+18005550100')
    return jsonify({"response": response_message})

def send_sms(api_key, content, from_number, to_number):
    url = "https://api.httpsms.com/v1/messages/send"
    headers = {
        "x-api-key": api_key,
        "Content-Type": "application/json"
    }
    payload = {
        "content": content,
        "from": from_number,
        "to": to_number
    }
    response = requests.post(url, json=payload, headers=headers)
    return response.json()

if __name__ == '__main__':
    app.run(debug=True)
