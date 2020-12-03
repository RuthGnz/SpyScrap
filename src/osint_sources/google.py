from selenium.webdriver.common.keys import Keys
import time
import urllib.request
from urllib.parse import unquote
from selenium import webdriver
import os
import json
import datetime
import face_recognition
from os import listdir,remove
from os.path import isfile, join
from selenium.webdriver.chrome.options import Options
from osint_sources.recognition import *
import spacy
import requests as req
import re

def containsAny(str, set):
    """ Check whether sequence str contains ANY of the items in set. """
    return 1 in [c in str for c in set]

def google(toSearch,placeToSearch,knownImage,number,verbose):
	chrome_options = Options()
	chrome_options.add_argument("--headless")
	chrome_options.add_argument("--no-sandbox")
	chrome_options.add_argument("--disable-dev-shm-usage")
	chrome_path = './chromedriver'
	driver = webdriver.Chrome(chrome_path,chrome_options=chrome_options)
	if placeToSearch != None and len(placeToSearch)>0:
		driver.get("https://www.google.com/search?q=site:"+placeToSearch+"+AND+%22"+toSearch+"%22&source=lnms&tbm=isch&sa=X&ved=0ahUKEwiz2eSN_9vgAhUJoRQKHU8YCuwQ_AUIDigB&biw=1181&bih=902")
	else:
		driver.get("https://www.google.com/search?q="+toSearch+"&source=lnms&tbm=isch&sa=X&ved=0ahUKEwiz2eSN_9vgAhUJoRQKHU8YCuwQ_AUIDigB&biw=1181&bih=902")

	driver.implicitly_wait(50)

    isMoreButton=True
	while isMoreButton:
		for i in range(1,10):
			driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
			time.sleep(2)


		inputs=driver.find_elements_by_tag_name('input')
		input_elem=None
		for inp in inputs:
			more=inp.get_attribute("type")
			if more=='button':
				input_elem=inp
				break
		if input_elem==None:
			isMoreButton=False
		else:
			print('More Elements')
			try:
				input_elem.click()
			except:
				break

	out = []
	jsonfile={}
	t =""
	my_set = {"{", "}", "&", "#", "_", "=",":","(",")", "+","."}
	nlp = spacy.load("es_core_news_sm")
	search=driver.find_elements_by_xpath("//img[contains(@class,'Q4LuWd')]")
	j=1
	notRepeatPhotos = []
	notRepeatFromUrl = []

	now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	if not os.path.isdir("data/google"):
		os.mkdir( "data/google");
	os.mkdir("data/google/"+str(now)+"_images")
	if number == None:
		number=len(search)

	img_urls=set()
	for i in  range(0,len(search)):
		img=search[i]
		try:
			img.click()
			time.sleep(2)
			actual_images = driver.find_elements_by_css_selector('img.n3VNCb')
			for actual_image in actual_images:
				if actual_image.get_attribute('src') and 'https' in actual_image.get_attribute('src'):
					url_image = actual_image.get_attribute('src')
					text_image = actual_image.get_attribute('alt')
					n = actual_image.find_element_by_xpath('..')
					url_content = n.get_attribute("href")
					jsonfile["photos"]=url_image
					jsonfile["from_url"]=url_content
					jsonfile["info"] = text_image
					if not url_content.endswith(".pdf"):
						try:
							resp = req.get(url_content)
							content = resp.text
							stripped = re.sub('<[^<]+?>', '', content)
							stripped_filter = re.sub('\n', '', stripped)
							stripped_filter2 = re.sub('\t', '', stripped_filter)
							doc = nlp(stripped_filter2)
							locs = []
							for e in doc.ents:
								if e.label_ == "LOC":
									if not containsAny(e.text,my_set) and not e.text in locs:
										locs.append(e.text)
							jsonfile["LOC_LIST"] = locs
						except:
							pass
					else:
						jsonfile["LOC_LIST"] = []

					if placeToSearch != None:
						name=os.path.join('data/google/'+str(now)+'_images',str(i)+"-"+placeToSearch+"-"+toSearch+".jpg")
					else:
						name=os.path.join('data/google/'+str(now)+'_images',str(i)+"-"+toSearch+".jpg")

					try:
						print(url_image)
						urllib.request.urlretrieve(url_image, name)
						jsonfile['storedImage']=name
					except:
						src=actual_image.get_attribute('src')
						if src != None:
							urllib.request.urlretrieve(src, name)
							jsonfile['storedImage']=name
					out.append(jsonfile)
					jsonfile={}
		except Exception as er:
			print(er)


	path= os.path.join('data/google',str(now)+'_google_data.json')
	response={'results':str(path)}
	with open(path, 'w+') as outfile:
		json.dump(out, outfile)
	print("Results Google in: " + str(path))
	if verbose:
		print(out)
	if knownImage:
		face_identification(knownImage,'data/google/'+str(now)+'_images/')
		response['images']='./data/google/'+str(now)+'_images/'
		response['recognized']='./data/google/'+str(now)+'_images/recognized/'
	return response
