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

def google(toSearch,placeToSearch,knownImage):
	print(toSearch)
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
	search=driver.find_elements_by_tag_name('img')
	j=1
	print('Retrieving images')
	now = datetime.datetime.now()
	os.mkdir( "images/"+str(now) );
	for s in search:

		td_p_input = s.find_element_by_xpath('..')
		link=td_p_input.get_attribute('href')
		div = td_p_input.find_element_by_xpath('..')
		
		if 'Q7Rsec'== div.get_attribute('jscontroller'):
			jsonDiv=div.find_elements_by_class_name('notranslate')[0]
			jsonInfo= json.loads(jsonDiv.get_attribute('innerHTML'))
			print(jsonInfo)
		try:
			listtext = driver.find_element_by_xpath("//*[@id=\"rg_s\"]/div["+str(j)+"]/a[2]")
			t = listtext.text
		except:
			pass
		if link != None:
			url=link.split('imgurl=')
			if len(url)>1:
				imgUrl=url[1].split('&')[0]
				imgUrl = unquote(imgUrl)
				if placeToSearch != None:
					name=os.path.join('images/'+str(now),str(j)+"-"+placeToSearch+"-"+toSearch+".jpg")
				else:
					name=os.path.join('images/'+str(now),str(j)+"-"+toSearch+".jpg")
				jsonfile[name]=imgUrl
				jsonfile["info"] = t
				t=""
				if knownImage != None:
					try:
						urllib.request.urlretrieve(imgUrl, name)
					except:
						src=s.get_attribute('src')
						if src != None:
							urllib.request.urlretrieve(src, name)
				j=j+1
				out.append(jsonfile)
				jsonfile={}
	path=os.path.join('images/'+str(now),'google_data.json')
	if not knownImage:
		with open(path, 'w+') as outfile:
			json.dump(out, outfile)
	else:
		openface_identification(knownImage,path)
