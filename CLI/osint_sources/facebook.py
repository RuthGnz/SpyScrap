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


def facebook (name_to_search):
    print(name_to_search)
    now = datetime.datetime.now()
    os.mkdir( "images/"+str(now) );
    path=os.path.join('images/'+str(now),'facebook_data.json')
    chrome_options = Options()
    jsonData=[]
    #chrome_options.add_argument("--headless")

    chrome_path = './chromedriver_linux64/chromedriver'
    driver = webdriver.Chrome(chrome_path,chrome_options=chrome_options)

    driver.get("https://es-la.facebook.com/public/"+name_to_search)
    driver.implicitly_wait(20)
    
    isMoreButton=True
    while isMoreButton:
        for i in range(1,10):
            isEnd=driver.find_elements_by_id('browse_end_of_results_footer')
            if len(isEnd)>0:
                isMoreButton=False
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
    links=[]
    print('*****Profiles Found*****')
    results=driver.find_elements_by_id('BrowseResultsContainer')[0]
    info=results.find_elements_by_tag_name('a')

    for user in info:
        user_class=user.get_attribute('class')
        if user_class=='_32mo':
            links.append(user.get_attribute('href'))
            print(user.get_attribute('href'))

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
                    print(user.get_attribute('href'))


    for l in links:
        driver.get(l)
        cover=driver.find_elements_by_class_name('coverPhotoImg')
        img=""
        if len(cover)>0:
            cover=cover[0]
            img=str(l)+".jpg"
            url=cover.get_attribute('src')
            print(url)
            image=os.path.join('images/'+str(now),img)
            try:
                urllib.request.urlretrieve(url, image)
            except:
                pass
            
        user={'image':img,'profile':l}
        jsonData.append(user)

    driver.quit()
