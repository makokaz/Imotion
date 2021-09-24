from app import app
from flask import Flask, request, render_template,jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, supports_credentials=True)
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)