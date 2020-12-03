from back_model import *
from werkzeug.utils import secure_filename
import os
from os import listdir,remove
from PIL import Image
import requests
from io import BytesIO
from selenium.webdriver.common.keys import Keys
import time
from selenium import webdriver
import os
import json
#from api import app
import sys
from osint_sources.scraper import *
from osint_sources.recognition import *
import datetime
import urllib.request
import shutil
import re
import logging


def allowed_file(filename,app):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def getValidImagePath(knownFiles,app):
	location0=None
	for f in knownFiles:
		file = knownFiles[f]
		if file and allowed_file(file.filename,app):
			filename = secure_filename(file.filename)
			location0 = os.path.join(app.config['UPLOAD_FOLDER'], filename)
			file.save(location0)
			known_image = face_recognition.load_image_file(location0)
			face_locations= face_recognition.face_locations(known_image)
			if len(face_locations)>0:
				break
	return location0


def compareImages(knownFiles,users,app):
	now = datetime.datetime.now()
	if users==None:
		photos=Photos_back.getPhotos()
	else:
		photos=Photos_back.getPhotosByUsers(users)


	for f in knownFiles:
		file = knownFiles[f]
		if file and allowed_file(file.filename,app):
			filename = secure_filename(file.filename)
			location0 = os.path.join(app.config['UPLOAD_FOLDER'], filename)
			file.save(location0)
			known_image = face_recognition.load_image_file(location0)
			face_locations= face_recognition.face_locations(known_image)
			if len(face_locations)>0:
				break
	folder=app.config['UPLOAD_FOLDER']+'/'+str(now)+'/'
	#save fotos in folder
	os.mkdir( folder);
	for i,p in enumerate(photos):
		try:
			location = os.path.join(folder, str(p['user']['id'])+'-'+str(i)+'.jpg')
			urllib.request.urlretrieve(p['photo'], location)
		except:
			pass
	face_identification(location0,folder)
	##get userIds from folder
	##remove photos
	userIds=[]

	# r=root, d=directories, f = files
	for r, d, f in os.walk(folder+'recognized'):
		for file in f:
			if '.jpg' in file:
				file=file.split('-')[0]
				userIds.append(int(file))

	users = User_Back.getById(userIds)
	remove(location0)
	shutil.rmtree(folder)
	return users

def getUsersByPhotoAndCompany(company,knownFiles,app):
	users = User_Back.getUserIdsByCompany(company)
	result=compareImages(knownFiles,users,app)
	return result

def getUsersByNameAndPhoto(name,knownFiles,app):
	result = []
	users = User_Back.getUserIdsByName(name)
	result = compareImages(knownFiles,users,app)
	return result

def getUsersNameCompanyPhoto(company,name,knownFiles,app):
	users = User_Back.getUsersIdsByCompanyAndName(company,name)
	result = compareImages(knownFiles,users,app)
	return result

def getUsersByCompany(company):
	ids = User_Back.getByJob(company)
	return ids

def getUsersByCompanyAndName(company,name):
	users = User_Back.getByCompanyAndName(company,name)
	return users

def getUsersByName(name):
	users = User_Back.getByName(name)
	return users


def getUsersByCompanyAndNameAndImage(company,name,knownFiles):
	pass



def google_controller(toSearch,placeToSearch,number,knownFiles,app):
	if number =="" or number=="undefined":
		number=None
	if placeToSearch == "" or placeToSearch=="undefined":
		placeToSearch=None
	if type(knownFiles)== str:
		knownImage=knownFiles
	else:
		if knownFiles == None:
			knownImage='file'
		elif len(knownFiles)>0:
			knownImage=getValidImagePath(knownFiles,app)
		else:
			knownImage=None
	paths=google(toSearch,placeToSearch,knownImage,number,False)
	jsonPath=paths['results']
	response={}
	with open(jsonPath) as json_file:
		data = json.load(json_file)

	if "recognized" in paths and knownImage!='file':
		files=[]
		for r, d, f in os.walk(paths['recognized']):
			for file in f:
				files.append(file)
		newData = []
		for a in data:
			try:
				img = a['storedImage'].split('/')
				img= img[len(img)-1]
				if img in files:
					path=a['storedImage'].split(img)[0]
					path=path+"recognized/"+img
					a['storedImage']=path
					newData.append(a)
			except:
				pass
		data=newData
	response['data']=data
	return response
def instagram_controller(toSearch,knownFiles,app):
	if type(knownFiles)== str:
		knownImage=knownFiles
	else:
		if knownFiles == None:
			knownImage='file'
		elif len(knownFiles)>0:
			knownImage=getValidImagePath(knownFiles,app)
		else:
			knownImage=None
	paths = instagram(toSearch,knownImage,False)
	jsonPath=paths['results']

	response={}

	with open(jsonPath) as json_file:
		data = json.load(json_file)


	if "recognized" in paths and knownImage!='file':
		files=[]
		for r, d, f in os.walk(paths['recognized']):
			for file in f:
				files.append(file)
		newData = []
		for a in data:
			try:
				img = a['image'].split('/')
				img= img[len(img)-1]
				if img in files:
					path=a['image'].split(img)[0]
					path=path+"recognized/"+img
					a['image']=path
					newData.append(a)
			except:
				pass
		data=newData
	response['data']=data
	return response

def twitter_controller(name_to_search,knownFiles,page_number,app):
	if type(knownFiles)== str:
		knownImage=knownFiles
	else:
		if knownFiles == None:
			knownImage='file'
		elif len(knownFiles)>0:
			knownImage=getValidImagePath(knownFiles,app)
		else:
			knownImage=None
	paths=twitter(name_to_search,page_number,knownImage,False)
	jsonPath=paths['results']
	response={}
	with open(jsonPath) as json_file:
		data = json.load(json_file)

	if "recognized" in paths and knownImage!='file':
		files=[]
		for r, d, f in os.walk(paths['recognized']):
			print(f)
			for file in f:
				files.append(file)
		newData = []
		for a in data:
			try:
				img = a['storedImage'].split('/')
				img= img[len(img)-1]
				if img in files:
					path=a['storedImage'].split(img)[0]
					path=path+"recognized/"+img
					a['storedImage']=path
					newData.append(a)
			except:
				pass
		data=newData
	response['data']=data
	return response

def facebook_controller(name_to_search,knownFiles,page_number,app):
	if type(knownFiles)== str:
		knownImage=knownFiles
	else:
		if knownFiles == None:
			knownImage='file'
		elif len(knownFiles)>0:
			knownImage=getValidImagePath(knownFiles,app)
		else:
			knownImage=None
	paths=facebook(name_to_search,knownImage,page_number,False)
	jsonPath=paths['results']
	response={}
	with open(jsonPath) as json_file:
		data = json.load(json_file)

	if "recognized" in paths and knownImage!='file':
		files=[]
		for r, d, f in os.walk(paths['recognized']):
			for file in f:
				files.append(file)
		newData = []
		for a in data:
			try:
				img = a['image'].split('/')
				img= img[len(img)-1]
				if img in files:
					path=a['image'].split(img)[0]
					path=path+"recognized/"+img
					a['image']=path
					newData.append(a)
			except:
				pass
		data=newData
	response['data']=data
	return response

def yandex_controller(url,knownFiles,token,app):
	logging.warning('URL '+url)
	if url != None:
		image = url
	elif type(knownFiles)== str:
		knownImage=knownFiles
	else:
		if knownFiles == None:
			knownImage='file'
		elif len(knownFiles)>0:
			knownImage=getValidImagePath(knownFiles,app)
		else:
			knownImage=None
		image=""
		if token== None and knownImage==None:
			return "error"
		else:
			image=knownImage
	print(image)
	paths=yandex(image,token,False)
	response={}
	jsonPath=paths['results']
	with open(jsonPath) as json_file:
		data = json.load(json_file)
		response['data']=data
	return response

def boe_controller(text,is_explicit,initDate,outDate,pages):
	paths=boe (text,initDate,outDate,pages,is_explicit,False)
	response={}
	jsonPath=paths['results']
	with open(jsonPath) as json_file:
		data = json.load(json_file)
		response['data']=data
	return response

def scoring_controller(name,url,number,gnumber,files,app):
	imagePath=getValidImagePath(files,app)
	response = {}
	try:
		ins = instagram_controller(name,imagePath,app)
		response['instagram']=ins['data']
	except:
		print('instagram error')
		response['instagram']=[]

	try:
		fb = facebook_controller(name,imagePath,number,app)
		response['facebook']=fb['data']
	except:
		print('facebook error')
		response['facebook']=[]

	try:
		gl = google_controller(name,"undefined",gnumber,imagePath,app)
		response['google']=gl['data']
	except:
		print('google error')
		response['google']=[]
	try:
		tw = twitter_controller(name,imagePath,number,app)
		response['twitter']=tw['data']
	except:
		print('twitter error')
		response['twitter']=[]
	try:
		yn = yandex_controller(url,None,None,app)
		response['yandex']=yn['data']
	except:
		print('yandex error')
		response['yandex']=[]


	score=compute_score(response)
	response['score']=score
	return response

def compute_score(data):
	#TODO
	#TOTAL 100
	#Twitter 10
	#Instagram 10
	#Facebook 10
	#Yandex 10 ->
	#Google 60
	score=0
	if len(data['twitter'])>0:
		score=score+10
	if len(data['facebook'])>0:
		score=score+10
	if len(data['instagram'])>0:
		score=score+10

	if data['yandex'] != False:
		if len(data['yandex'])>0:
			yn=data['yandex']
			score=score+1
			bonus=0
			if len(yn)>10:
				bonus=bonus+1
			if len(yn)>20:
				bonus=bonus+2
			if len(yn)>30:
				bonus=bonus+3;
			if len(yn)>40:
				bonus=bonus+3;
			score=score+bonus


	if len(data['google'])>0:

		gn=data['google']
		score=score+10
		bonus=0
		if len(gn)>2:
			bonus=bonus+5
		elif len(gn)>5:
			bonus=bonus+5
		elif len(gn)>10:
			bonus=bonus+5;
		elif len(gn)>15:
			bonus=bonus+5;
		elif len(gn)>25:
			bonus=bonus+5;
		elif len(gn)>35:
			bonus=bonus+5;
		elif len(gn)>45:
			bonus=bonus+5;
		elif len(gn)>55:
			bonus=bonus+5;
		elif len(gn)>65:
			bonus=bonus+5;
		elif len(gn)>75:
			bonus=bonus+5;
	return score
