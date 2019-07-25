#!/usr/bin/python
# coding: utf-8
# encoding=utf8
import sys
import datetime
import time
import os
import requests
import json

def instagram (name_to_search):
    resp = requests.get(url='https://www.instagram.com/web/search/topsearch/?context=blended&query='+name_to_search)
    now = datetime.datetime.now()
    os.mkdir( "images/"+str(now) );
    path=os.path.join('images/'+str(now),'instagram_data.json')
    print('*******Results*******')
    users=resp.json()['users']
    jsonData=[]
    for u in users:
        user={'username:':u['user']['username'],'full_name':u['user']['full_name'],'profile':'https://www.instagram.com/'+u['user']['username'],'is_private':u['user']['is_private'],'is_verified':u['user']['is_verified']}
        print('Username: '+u['user']['username'])
        print('Full Name: '+u['user']['full_name'])
        print('Profile: https://www.instagram.com/'+u['user']['username'])
        print('Is Private: '+str(u['user']['is_private']))
        print('Is Verified: '+str(u['user']['is_verified']))
        print()
        jsonData.append(user)
    with open(path, 'w+') as outfile:
        json.dump(jsonData, outfile)     

   