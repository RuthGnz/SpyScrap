from flask import Flask, jsonify, request
import requests
import logging
import json
from flask_cors import CORS
from controller import *


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './uploads'
app.config['ALLOWED_EXTENSIONS'] = ['png','jpeg','jpg']
CORS(app)

URL_BASE = '/osint/api/v1'

@app.route("/osint/api/v1")
def ping():
    return "It works OSINT!"


@app.route(URL_BASE+"/tinder",methods=['POST'])
def tinder():
	
	name = request.form.get('name')
	company = request.form.get('company')
	files = request.files
	users = []
	if len(files)>0 and not name and not company:
		users=compareImages(files,None)
	if company and not name and len(files)==0:
		users = getUsersByCompany(company)
	elif name and not company and len(files)==0:
		users = getUsersByName(name)
	elif company and name and len(files)==0:
		users = getUsersByCompanyAndName(company,name)
	elif company and name and len(files)>0:
		users=getUsersNameCompanyPhoto(company,name,files)
	elif company and not name and len(files)>0:
		users=getUsersByPhotoAndCompany(company,files)
	elif not company and name and len(files)>0:
		users=getUsersByNameAndPhoto(name,files)

	return jsonify({'msg':users})

@app.route(URL_BASE+"/google",methods=['POST'])
def google():
	data=[]
	name = request.form.get('name')
	place = request.form.get('place')
	files = request.files
	google_controller(name,place,files)
	return jsonify({'msg':data})

if __name__ == '__main__':
    app.run(debug=True)