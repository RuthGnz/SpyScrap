from model import *
import face_recognition
from werkzeug.utils import secure_filename
import os
from api import app
from PIL import Image
import requests
from io import BytesIO

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def compareImages(knownFiles):
	##Todo cambiar nombre y borrar fotos al acabar
	print('entra')
	photos=Photos.getPhotos()

	print('aqui')
	for f in knownFiles:
		file = knownFiles[f]
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			location = os.path.join(app.config['UPLOAD_FOLDER'], filename)
			file.save(location)
			known_image = face_recognition.load_image_file(location)
			face_locations= face_recognition.face_locations(known_image)
			if len(face_locations)>0:
				break
	for p in photos:
		response = requests.get(p['photo'])
		img = None
		try:
			img = Image.open(BytesIO(response.content))
		except:
			#image deleted
			print('deleted image')

		if img!=None:
			filenameArr = p['photo'].split('/')
			index = len(filenameArr)-1
			filename = filenameArr[index]
			location = os.path.join(app.config['UPLOAD_FOLDER'], filename)
			img.save(location)
	return []
'''		
		
		
		unknown_image = face_recognition.load_image_file(location)

		try:
			biden_encoding = face_recognition.face_encodings(known_image)[0]
			if len(face_recognition.face_encodings(unknown_image))>0:
				unknown_encoding = face_recognition.face_encodings(unknown_image)[0]

				results = face_recognition.compare_faces([biden_encoding], unknown_encoding)
				if results[0]==True:
					print(f)
					newJsonData[f]=jsondata[join('images',f)]
				else:
					pass
					##Puede reconocer mal
					#remove(join('./images', f))
			else:
				pass
				##Puede haber alguna que si que sea un rostro
				#remove(join('./images', f))
		except:
			pass
			#remove(join('./images', f))		'''
	#coger dos imagenes que tengan cada de un usuario y compararlas conla imagen q te dan si es march devuelve todas las imagenes
	#return []

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