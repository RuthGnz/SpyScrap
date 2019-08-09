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
from difflib import SequenceMatcher
from osint_sources.recognition import *

def twitter (name_to_search,page_number,knownimage,verbose):

    placeToSearch='twitter.com'
    chrome_options = Options()
    chrome_options.add_argument("--headless")

    chrome_path = './chromedriver'
    driver = webdriver.Chrome(chrome_path,chrome_options=chrome_options)

    people_list=[]
    for i in range(int(page_number)):
        driver.get("https://www.google.com/search?q=site:"+placeToSearch+"+AND+"+name_to_search + "&start=" + str(10 * i))
        search=driver.find_elements_by_tag_name('cite')
        time.sleep(10)
        for s in search:
            if "https://twitter.com/" in s.text:
                if "/status/" not in s.text and "/media" not in s.text:
                    people_list.append(s.text)
                else:
                    if "/status/" in s.text:
                        people_list.append(s.text.split("/status/")[0])
                    elif "/media" not in s.text:
                        people_list.append(s.text.split("/media")[0])


    people_list=set(people_list)
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if not os.path.isdir("data/twitter"):
        os.mkdir("data/twitter");

    path=os.path.join('data/twitter',str(now)+'_twitter_data.json')
    jsonData=[]
    for p in people_list:
        if verbose:
            print("*******************************************************************************************************")
            print(p)
        driver.get(p)
        driver.implicitly_wait(50)
        time.sleep(2)

        sel = Selector(text=driver.page_source)
        "ProfileHeaderCard-nameLink u-textInheritColor js-nav"
        name = sel.xpath('//*[starts-with(@class, "ProfileHeaderCard-nameLink u-textInheritColor js-nav")]/text()').extract_first()
        link = sel.xpath('//*[starts-with(@class, "u-linkComplex-target")]/text()').extract_first()
        description = sel.xpath('//*[starts-with(@class, "ProfileHeaderCard-bio u-dir")]/text()').extract_first()
        location = sel.xpath('//*[starts-with(@class, "ProfileHeaderCard-locationText u-dir")]/a/text()').extract_first()
        if location == None:
            location = sel.xpath('//*[starts-with(@class, "ProfileHeaderCard-locationText u-dir")]/text()').extract_first()
        member_since = sel.xpath('//*[starts-with(@class, "ProfileHeaderCard-joinDateText js-tooltip u-dir")]/text()').extract_first()
        activity = sel.xpath('//*[starts-with(@class, "PhotoRail-headingWithCount js-nav")]/text()').extract_first()
        born=sel.xpath('//*[starts-with(@class, "ProfileHeaderCard-birthdateText u-dir")]/span/text()').extract_first()
        webpage=sel.xpath('//*[starts-with(@class, "ProfileHeaderCard-urlText u-dir")]/a/@title').extract_first()
        image_url=sel.xpath('//img[@class="ProfileAvatar-image "]/@src').extract_first()
        if name==None:
            name=""
        if SequenceMatcher(None,name_to_search, name).ratio()>0.8 or name_to_search in str(description).lower():
            if verbose:
                print("Name: "+str(name))
                print("Link: "+str(link))
                print("Description: "+str(description))
                print("Location: "+ str(location))
                print("Member since: "+str(member_since))
                print("Activity: "+str(activity))
                print("Born: "+str(born))
                print("Web: "+str(webpage))
                print ("Profile image url: "+str(image_url))
                print('\n')
                print('\n')
            userData={'name':str(name),'link':str(link),'description':str(description),'location':str(location),'member_since':str(member_since),'activity':activity,'born':str(born),'web':str(webpage),'image':str(image_url)}
            jsonData.append(userData)
            if knownimage:
                if not os.path.isdir("data/twitter/"+str(now)+"_images"):
                    os.mkdir("data/twitter/"+str(now)+"_images");
                image=os.path.join("data/twitter/"+str(now)+"_images",placeToSearch+"-"+str(link)+".jpg")
                try:
                    urllib.request.urlretrieve(image_url, image)
                except:
                    pass
    with open(path, 'w+') as outfile:
        json.dump(jsonData, outfile)

    print("Results Twitter in: " + str(path))
    response={'results':str(path)}
    if knownimage:
        print("Compare similarity images.")
        openface_identification(knownimage,'./data/twitter/'+str(now)+'_images/')
        response['images']='./data/twitter/'+str(now)+'_images/'
        response['recognized']='./data/twitter/'+str(now)+'_images/recognized/'
    driver.quit()

    return response