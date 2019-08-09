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

def google(toSearch,placeToSearch,knownImage,verbose):
	chrome_options = Options()
	chrome_options.add_argument("--headless")
	chrome_path = './chromedriver'
	driver = webdriver.Chrome(chrome_path,chrome_options=chrome_options)
	if placeToSearch != None:
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
	search=driver.find_elements_by_tag_name('img')
	j=1
	notRepeatPhotos = []
	notRepeatFromUrl = []
	print('Retrieving images')
	now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	if not os.path.isdir("data/google"):
		os.mkdir( "data/google");
	os.mkdir("data/google/"+str(now)+"_images")
	for s in search:

		td_p_input = s.find_element_by_xpath('..')
		link=td_p_input.get_attribute('href')
		div = td_p_input.find_element_by_xpath('..')
		if link != None:
			url=link.split('imgurl=')
			if len(url)>1:
				imgUrl=url[1].split('&')[0]
				if not imgUrl in notRepeatPhotos:
					notRepeatPhotos.append(imgUrl)
					if 'Q7Rsec'== div.get_attribute('jscontroller'):
						jsonDiv=div.find_elements_by_class_name('notranslate')[0]
						jsonInfo= json.loads(jsonDiv.get_attribute('innerHTML'))
						from_url = jsonInfo["ru"]
						if not from_url in notRepeatFromUrl:
							notRepeatFromUrl.append(from_url)
							imgUrl = unquote(imgUrl)
							jsonfile["photos"]=imgUrl
							jsonfile["from_url"] = from_url
							if not from_url.endswith(".pdf"):
    								try:
    									resp = req.get(from_url)
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
    									locs = []

    									listtext = driver.find_element_by_xpath("//*[@id=\"rg_s\"]/div["+str(j)+"]/a[2]")
    									t = listtext.text
    									jsonfile["info"] = t
    									t =""
    								except:
    									pass


							else:
    								jsonfile["LOC_LIST"] = []
							out.append(jsonfile)
							jsonfile={}

					if placeToSearch != None:
						name=os.path.join('data/google/'+str(now)+'_images',str(j)+"-"+placeToSearch+"-"+toSearch+".jpg")
					else:
						name=os.path.join('data/google/'+str(now)+'_images',str(j)+"-"+toSearch+".jpg")

					if knownImage != None:
						try:
							urllib.request.urlretrieve(imgUrl, name)
						except:
							src=s.get_attribute('src')
							if src != None:
								urllib.request.urlretrieve(src, name)
					j=j+1


	path= os.path.join('data/google',str(now)+'_google_data.json')
	with open(path, 'w+') as outfile:
		json.dump(out, outfile)
	print("Results Google in: " + str(path))
	if verbose:
		print(out)
	if knownImage:
		openface_identification(knownImage,'data/google/'+str(now)+'_images')
