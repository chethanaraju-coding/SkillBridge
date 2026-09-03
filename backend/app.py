from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app) # This allows your React frontend to talk to this backend

@app.route('/')
def home():
    return jsonify({"message": "SkillBridge API is running successfully!"})

@app.route('/api/data')
def get_data():
    return jsonify({"status": "success", "data": "This is data from the backend!"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)