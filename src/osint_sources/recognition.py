import face_recognition
from os import listdir,remove
from os.path import isfile, join
import os
import cv2
import numpy as np

def face_identification(known_image,folder):
	#print('****** Image recognition *******')
	onlyfiles = [join(folder, f) for f in listdir(folder) if isfile(join(folder, f))]

	try:
		known_image_recon = face_recognition.load_image_file(known_image)
		known_encoding = face_recognition.face_encodings(known_image_recon)[0]

	except:
		print('Not valid known image')
		return

	os.mkdir( folder+'recognized/');


	for image in onlyfiles:
		if 'data.json' not in image:

			unknown_image = face_recognition.load_image_file(image)

			if len(face_recognition.face_encodings(unknown_image))>0:
				unknown_encoding = face_recognition.face_encodings(unknown_image)[0]
				results = face_recognition.compare_faces([known_encoding], unknown_encoding)
				if results[0]==True:
					img_name=image.split('/')
					img_name=img_name[len(img_name)-1]
					new_image=folder+'/recognized/'+img_name
					os.rename(image,new_image)
				else:
					pass
			else:
				pass
				#print('Not face found')
		else:
			pass
	#print()
