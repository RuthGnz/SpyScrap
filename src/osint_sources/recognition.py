import face_recognition
from os import listdir,remove
from os.path import isfile, join
import os
import cv2
import openface
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


modelDir = os.path.join('./openface/', 'models')
dlibModelDir = os.path.join(modelDir, 'dlib')
openfaceModelDir = os.path.join(modelDir, 'openface')

def openface_identification(known_image,folder):
	#todo resize 100x100 to speedup
	os.mkdir( folder+'recognized/');

	threshold=0.6
	response=[]
	imgDim=96
	align = openface.AlignDlib(os.path.join(dlibModelDir, "shape_predictor_68_face_landmarks.dat"))
	net = openface.TorchNeuralNet(os.path.join(openfaceModelDir, 'nn4.small2.v1.t7'),imgDim)
	rep1=getRep(known_image,align,net,imgDim)
	onlyfiles = [join(folder, f) for f in listdir(folder) if isfile(join(folder, f))]
	for image in onlyfiles:
		if 'jpeg' in image or 'jpg' in image or 'png' in image:
			rep2=getRep(image,align,net,imgDim)
			if len(rep2)>0 and len(rep1)>0:
				d= rep1-rep2
				res=np.dot(d, d)
				if res <= threshold:
					response.append(image)

	for image in response:
		img_name=image.split('/')
		img_name=img_name[len(img_name)-1]
		new_image=folder+'recognized/'+img_name
		os.rename(image,new_image)
	return response



def getRep(imgPath,align,net,imgDim):
	bgrImg = cv2.imread(imgPath)
	if bgrImg is None:
		#raise Exception("Unable to load image: {}".format(imgPath))
		return []
	rgbImg = cv2.cvtColor(bgrImg, cv2.COLOR_BGR2RGB)
	bb = align.getLargestFaceBoundingBox(rgbImg)

	if bb is None:
		#print("Unable to find a face: {}".format(imgPath))
		return []

	alignedFace = align.align(imgDim, rgbImg, bb, landmarkIndices=openface.AlignDlib.OUTER_EYES_AND_NOSE)
	if alignedFace is None:
		#print("Unable to align image: {}".format(imgPath))
		return []

	rep = net.forward(alignedFace)
	return rep
