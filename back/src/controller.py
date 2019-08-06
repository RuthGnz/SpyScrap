from model import *
import face_recognition
from werkzeug.utils import secure_filename
import os
from os import listdir,remove
from PIL import Image
import requests
from io import BytesIO
from selenium.webdriver.common.keys import Keys
import time
import urllib.request
from urllib.parse import unquote
from selenium import webdriver
import os
import json
from app import app

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


#####TODOOOOOOOOOOOO
##si da tres negativos dejar de comparar con ese usuario
##si da tres positivos es ok
##hilos 
##si tarda mucho el front peta
def compareImages(knownFiles,users):
	##Todo cambiar nombre y borrar fotos al acabar
	usersCompared={}
	if users==None:
		photos=Photos.getPhotos()
	else:
		photos=Photos.getPhotosByUsers(users)
	failedUsers={}
	userIds=[]
	for f in knownFiles:
		file = knownFiles[f]
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			location0 = os.path.join(app.config['UPLOAD_FOLDER'], filename)
			file.save(location0)
			known_image = face_recognition.load_image_file(location0)
			face_locations= face_recognition.face_locations(known_image)
			if len(face_locations)>0:
				break
	for p in photos:
		userCompared=p['user']['id']
		if userCompared in usersCompared.keys():
			pass
		else:
			pass
		userIdsFailed=failedUsers.keys()
		response = requests.get(p['photo'])
		img = None
		try:
			img = Image.open(BytesIO(response.content))
			filenameArr = p['photo'].split('/')
			index = len(filenameArr)-1
			filename = filenameArr[index]
			location = os.path.join(app.config['UPLOAD_FOLDER'], filename)
			img.save(location)
		except:
			#image deleted
			#print('deleted image')
			pass
		if img!=None:

			unknown_image = face_recognition.load_image_file(location)
			try:
				biden_encoding = face_recognition.face_encodings(known_image)[0]
				if len(face_recognition.face_encodings(unknown_image))>0:
					unknown_encoding = face_recognition.face_encodings(unknown_image)[0]

					results = face_recognition.compare_faces([biden_encoding], unknown_encoding)
					if results[0]==True:
						userIds.append(p['user']['id'])
						remove(location)
					else:
						##Puede reconocer mal, tener en cuenta
						remove(location)
				else:
					##Puede haber alguna que si que sea un rostro
					remove(location)
			except:
				remove(location)
	#remove(location0)
	users = User.getById(userIds)
	return users

def getUsersByPhotoAndCompany(company,knownFiles):
	users = User.getUserIdsByCompany(company)
	result=compareImages(knownFiles,users)
	return result

def getUsersByNameAndPhoto(name,knownFiles):
	result = []
	users = User.getUserIdsByName(name)
	result = compareImages(knownFiles,users)
	return result

def getUsersNameCompanyPhoto(company,name,knownFiles):
	users = User.getUsersIdsByCompanyAndName(company,name)
	result = compareImages(knownFiles,users)
	return result

def getUsersByCompany(company):
	ids = User.getByJob(company)
	return ids

def getUsersByCompanyAndName(company,name):
	users = User.getByCompanyAndName(company,name)
	return users

def getUsersByName(name):
	users = User.getByName(name)
	return users


def getUsersByCompanyAndNameAndImage(company,name,knownFiles):
	pass



def google_controller(toSearch,placeToSearch,knownImage):
	pass