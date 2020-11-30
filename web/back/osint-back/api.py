from flask import Flask, jsonify, request,send_from_directory
import logging
from controller import *
from flask_cors import CORS
app = Flask(__name__,static_url_path = "/data", static_folder = "./data")
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
		users=getUsersByNameAndPhoto(name,files,app)

	return jsonify({'msg':users})

@app.route(URL_BASE+"/google",methods=['POST'])
def google():
	data=[]
	name = request.form.get('name')
	download = request.form.get('download')
	number = request.form.get('number')
	if name == None:
		return jsonify("Name must me provided")
	place = request.form.get('place')
	files = request.files
	files = request.files
	if len(files)==0 and download=='true':
		files=None
	data=google_controller(name,place,number,files,app)
	return jsonify({'msg':data['data']})

@app.route(URL_BASE+"/instagram",methods=['POST'])
def instagram():
	data=[]
	name = request.form.get('name')
	download = request.form.get('download')

	if name == None:
		return jsonify("Name must me provided")
	files = request.files
	if len(files)==0 and download=='true':
		files=None
	data=instagram_controller(name,files,app)
	return jsonify({'msg':data['data']})


##todo
@app.route(URL_BASE+"/twitter",methods=['POST'])
def twitter():
	data=[]
	name = request.form.get('name')
	number = request.form.get('number')
	download = request.form.get('download')
	if name == None:
		return jsonify("Name must me provided")
	if number==None:
		number=1
	files = request.files
	if len(files)==0 and download=='true':
		files=None
	data=twitter_controller(name,files,number,app)
	return jsonify({'msg':data['data']})


@app.route(URL_BASE+"/facebook",methods=['POST'])
def facebook():
	data=[]
	name = request.form.get('name')
	number = request.form.get('number')
	download = request.form.get('download')
	if name == None:
		return jsonify("Name must me provided")
	if number==None:
		number=1
	files = request.files
	if len(files)==0 and download=='true':
		files=None
	data=facebook_controller(name,files,number,app)
	return jsonify({'msg':data['data']})

@app.route(URL_BASE+"/boe",methods=['POST'])
def boe():
	data=[]
	text = request.form.get('text')
	is_explicit = request.form.get('explicit')
	pages = request.form.get('pages')
	if text == None:
		return jsonify("Text must me provided")
	initDate=None
	outDate=None
	data=boe_controller(text,is_explicit,initDate,outDate,pages)
	return jsonify({'msg':data['data']})

@app.route(URL_BASE+"/yandex",methods=['POST'])
def yandex():
	data=[]
	url = request.form.get('url')
	token = request.form.get('token')
	files = request.files
	data=yandex_controller(url,files,token,app)
	return jsonify({'msg':data['data']})


@app.route(URL_BASE+"/data/<folder>/<dateFolder>/<image>")
def download_file(folder,dateFolder,image):

    return send_from_directory('./data/'+folder+'/'+dateFolder,image)

@app.route(URL_BASE+"/scoring",methods=['POST'])
def scoring():
	#TODO
	name = request.form.get('name')
	token = request.form.get('token')
	number = request.form.get('number')
	gnumber = request.form.get('gnumber')
	files = request.files
	if len(files)==0:
		return jsonify({'msg':'Image must be sent'}),400
	data=scoring_controller(name,token,number,gnumber,files,app)
	return jsonify({'msg':data})

if __name__ == '__main__':
    app.run(debug=True)
