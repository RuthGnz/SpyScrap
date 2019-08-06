from flask import Flask, jsonify, request
from flask_cors import CORS
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './uploads'
app.config['ALLOWED_EXTENSIONS'] = ['png','jpeg','jpg']
CORS(app)

