#!/usr/bin/python
# coding: utf-8
# encoding=utf8
import sys
import datetime
from selenium.webdriver.common.keys import Keys
import time
from selenium import webdriver
import os
from parsel import Selector
import urllib.parse
from selenium.common.exceptions import NoSuchElementException
import json
from selenium.webdriver.chrome.options import Options
import shutil
import requests
from osint_sources.recognition import *
def facebook (name_to_search,knownimage,size,verbose):

    chrome_options = Options()
    jsonData=[]
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    chrome_path = './chromedriver'
    driver = webdriver.Chrome(chrome_path,chrome_options=chrome_options)


    driver.get("https://es-la.facebook.com/public/"+name_to_search)
    print("https://es-la.facebook.com/public/"+name_to_search)
    driver.implicitly_wait(20)

    isMoreButton=True
    for i in range(1,int(size)):
        isEnd=driver.find_elements_by_id('browse_end_of_results_footer')
        print(isEnd)
        if len(isEnd)>0:
            isMoreButton=False
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
    links=[]
    results=driver.find_elements_by_id('BrowseResultsContainer')
    if len(results)>0:
        results=results[0]
        info=results.find_elements_by_tag_name('a')
    else:
        info=[]

    for user in info:
        user_class=user.get_attribute('class')
        if user_class=='_32mo':
            links.append(user.get_attribute('href'))
            user={'name':user.get_attribute('title'),'profile':user.get_attribute('href')}
            jsonData.append(user)

    isMoreButton=True
    i=0
    id_value="fbBrowseScrollingPagerContainer"
    while isMoreButton:
        more=driver.find_elements_by_id(id_value+str(i))
        i=i+1
        if len(more)==0:
            isMoreButton=False
        else:
            div = more[0]
            info=div.find_elements_by_tag_name('a')
            for user in info:
                user_class=user.get_attribute('class')
                if user_class=='_32mo':
                    links.append(user.get_attribute('href'))
                    user={'name':user.get_attribute('title'),'profile':user.get_attribute('href')}
                    jsonData.append(user)

    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if not os.path.isdir("data/facebook"):
        os.mkdir( "data/facebook");
    os.mkdir("data/facebook/"+str(now)+"_images")
    path= os.path.join('data/facebook',str(now)+'_facebook_data.json')
    with open(path, 'w+') as outfile:
        json.dump(jsonData, outfile)
    if verbose:
        print(jsonData)
    print("Results Facebook in: " + str(path))

    j=0
    response={'results':str(path)}
    if knownimage:
        for ind,l in enumerate(links):
            user=jsonData[ind]
            driver.get(l)
            try:
                div=driver.find_elements_by_class_name('profilePicThumb')[0]
                img=div.find_elements_by_tag_name('img')[0]
                url=img.get_attribute('src')
                name=os.path.join('data/facebook/'+str(now)+'_images',str(j)+"-"+name_to_search+".jpg")
                j=j+1
                urllib.request.urlretrieve(url, name)
                user['image']=name
            except:
                pass
        with open(path, 'w+') as outfile:
            json.dump(jsonData, outfile)
        driver.quit()
        print("Start compare images")

        face_identification(knownimage,'./data/facebook/'+str(now)+'_images/')
        response['images']='./data/facebook/'+str(now)+'_images/'
        response['recognized']='./data/facebook/'+str(now)+'_images/recognized/'

    return response
