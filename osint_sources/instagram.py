#!/usr/bin/python
# coding: utf-8
# encoding=utf8
import sys
import datetime
import time
import os
import requests
import json
import urllib.request
from osint_sources.recognition import *
def instagram (name_to_search,knownimage):
    resp = requests.get(url='https://www.instagram.com/web/search/topsearch/?context=blended&query='+name_to_search)
    now = datetime.datetime.now()
    os.mkdir( "images/"+str(now) );
    path=os.path.join('images/'+str(now),'instagram_data.json')
    print('*******Results*******')
    users=resp.json()['users']
    jsonData=[]
    j=0
    for u in users:
        print('Username: '+u['user']['username'])
        print('Full Name: '+u['user']['full_name'])
        print('Profile: https://www.instagram.com/'+u['user']['username'])
        print('Is Private: '+str(u['user']['is_private']))
        print('Is Verified: '+str(u['user']['is_verified']))
        print()
        if knownimage:
            image_name=os.path.join('images/'+str(now),str(j)+"-"+'instagram.jpg')
            urllib.request.urlretrieve(u['user']['profile_pic_url'], image_name)
            user={'username:':u['user']['username'],'full_name':u['user']['full_name'],'profile':'https://www.instagram.com/'+u['user']['username'],'is_private':u['user']['is_private'],'is_verified':u['user']['is_verified'],'image':image_name}
            j=j+1
        else:
            user={'username:':u['user']['username'],'full_name':u['user']['full_name'],'profile':'https://www.instagram.com/'+u['user']['username'],'is_private':u['user']['is_private'],'is_verified':u['user']['is_verified']}

        
        jsonData.append(user)
    with open(path, 'w+') as outfile:
        json.dump(jsonData, outfile)     

    if knownimage:
        openface_identification(knownimage,'./images/'+str(now)+'/')



        
 