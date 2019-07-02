from flask import Flask, jsonify, request
import requests
import logging
import json
from flask_cors import CORS
from controller import *


app = Flask(__name__)
CORS(app)

URL_BASE = '/osint/api/v1'

@app.route("/osint/api/v1")
def ping():
    return "It works OSINT!"


@app.route(URL_BASE+"/tinder",methods=['POST'])
def tinder():
	
	name = request.form.get('name')
	company = request.form.get('company')
	files = request.form.get('files')
	users = []
	if company and not name and len(files)==0:
		users = getUsersByCompany(company)

	return jsonify({'msg':users})

if __name__ == '__main__':
    app.run(debug=True)