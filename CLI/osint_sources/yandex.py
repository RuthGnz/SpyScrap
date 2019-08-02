from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from urllib.parse import unquote
from os.path import isfile, join
from os import listdir,remove
import time
import json
import os
import requests
import re
import datetime
import base64
import urllib.parse
import urllib.request
from urllib.request import Request, urlopen
import random
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

def isCaptcha(driver):
	headers=driver.find_elements_by_tag_name('h1')
	for h in headers:
		if h.get_attribute('innerHTML')=="oops…":
			print('captcha detected')
			return(True)
	return(False)

def checkProxy(proxy):

	#print(proxy)
	proxies = {
	"http": proxy,
	"https": proxy,
	}

	try:
		#print("Request to Google to try Proxy")
		resp= requests.get("https://google.com", proxies=proxies, timeout=20)
		print("Google responses "+str(resp.status_code)+" in "+str(resp.elapsed.total_seconds())+ " seconds.")
		if((resp.status_code!=200) or resp.elapsed.total_seconds()>10):
			#print("It takes a long time or error")
			return 0
		else:
			#print("It is a valid proxy")
			return 1
	except:
		print("Error while checking the proxy: "+ str(proxy))
		return 0

def crawlProxy():
	# Retrieve latest proxies
	ua = UserAgent()
	proxies = []
	proxies_req = Request('https://www.sslproxies.org/')
	proxies_req.add_header('User-Agent', ua.random)
	proxies_doc = urlopen(proxies_req).read().decode('utf8')

	soup = BeautifulSoup(proxies_doc, 'html.parser')
	proxies_table = soup.find(id='proxylisttable')

	# Save proxies in the array
	for row in proxies_table.tbody.find_all('tr'):
		proxies.append({ 'ip':   row.find_all('td')[0].string, 'port': row.find_all('td')[1].string})

	invalidProxy=True
	proxy = None
	while invalidProxy:
		random_index = random.randint(0, len(proxies) - 1)
		random_proxy = proxies[random_index]
		proxy = str(random_proxy['ip'])+":"+str(random_proxy['port'])
		chk=checkProxy(proxy)
		if chk:
			invalidProxy=False
	return proxy

def searchImages(driver):
	search=driver.find_elements_by_tag_name('img')
	j=0
	if len(search)<10:
		return (False)
	print('Retrieving images')
	out = []
	for s in search:
		try:
			link=s.get_attribute('src')
			if link != None and link != "":
				#name=os.path.join('images',str(j)+"-"+placeToSearch+".jpg")
				#urllib.request.urlretrieve(link, name)
				j=j+1
				div1 = s.find_element_by_xpath('..')
				div2 = div1.find_element_by_xpath('..')
				div3 = div2.find_element_by_xpath('..')
				databem=json.loads(div3.get_attribute('data-bem'))
				if databem is not None:
					originUrl=databem['serp-item']['preview'][0]['origin']['url']
					print(originUrl)
					dataOrigin=databem['serp-item']['snippet']
					title=dataOrigin['title']
					text = dataOrigin['text']
					url = dataOrigin['url']
					domain = dataOrigin['domain']
					info ={}
					info["originUrl"] = originUrl
					info["title"] = title
					info["text"] = text
					info["url"] = url
					info["domain"] = domain
					print("-----------------")
					print(info)
					out.append(info)


		except Exception as e:
			print("-----------------")
			print('Image witout Tag')

	return out

def deletedImage(hashimage, token):
    headers = {'Authorization': 'Client-ID ' + token}
    req = requests.delete(url= "https://api.imgur.com/3/image/" + hashimage, headers= headers)
    if req.status_code == requests.codes.ok:
        return True
    else:
        return False


def yandex(name,image,token):
	image_url = image
	image_delete = ""
	url = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+] |[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', image)
	if not url:
		try:
			f = open(image, "rb")
		except FileNotFoundError as e:
			print ("Image not found: " + image)
			sys.exit(-1)
		image_data = f.read()
		b64_image = base64.standard_b64encode(image_data)
		client_id = token
		headers = {'Authorization': 'Client-ID ' + token}
		data = {'image': b64_image, 'title': 'test'}
		try:
			request = requests.post(url="https://api.imgur.com/3/upload.json", data=data,headers=headers)
			if request.status_code == requests.codes.ok:
				image_url = request.json()['data']['link']
				image_delete = request.json()['data']['deletehash']
				print ("Image upload to imgur: " + image_url)
		except Exception as e:
			print(e)
			sys.exit(-1)


	proxy=crawlProxy()
	if proxy is not None:
		#proxy="81.163.62.136:41258"
		print (proxy)
		chrome_options = webdriver.ChromeOptions()
		chrome_options.add_argument('--proxy-server=%s' % proxy)
		chrome_path = './chromedriver'
		driver = webdriver.Chrome(chrome_path,options=chrome_options)
		url_final = "https://yandex.ru/images/search?url="+image_url+"&rpt=imagelike"
		driver.get(url_final)
		driver.implicitly_wait(50)
		time.sleep(3)
		captcha=isCaptcha(driver)
		if captcha == True:
			driver.close()
		else:
			images=searchImages(driver)
			if not images:
				print('No images.')
				driver.close()
		print("Closing the search")
		if deletedImage(image_delete,token):
			print ("Image deleted")
		else:
			print("Problem when deleted image from imgur")

	else:
		print('Yandex is blocked')
