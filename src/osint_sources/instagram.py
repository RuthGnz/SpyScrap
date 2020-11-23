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

def instagram (name_to_search,knownimage,verbose):
    resp = requests.get(url='https://www.instagram.com/web/search/topsearch/?context=blended&query='+name_to_search)
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if not os.path.isdir("data/instagram"):
        os.mkdir("data/instagram");

    path=os.path.join('data/instagram',str(now)+'_instagram_data.json')
    users=resp.json()['users']
    jsonData=[]
    j=0
    for u in users:
        if verbose:
            print('Username: '+u['user']['username'])
            print('Full Name: '+u['user']['full_name'])
            print('Profile: https://www.instagram.com/'+u['user']['username'])
            print('Is Private: '+str(u['user']['is_private']))
            print('Is Verified: '+str(u['user']['is_verified']))
            print()
        if knownimage:
            if not os.path.isdir("data/instagram/"+str(now)+"_images"):
                os.mkdir("data/instagram/"+str(now)+"_images");
            image_name=os.path.join('data/instagram/'+str(now)+'_images',str(j)+"-"+'instagram.jpg')
            try:
                urllib.request.urlretrieve(u['user']['profile_pic_url'], image_name)
            except Exception as e:
                print(e)

            user={'username':u['user']['username'],'full_name':u['user']['full_name'],'profile':'https://www.instagram.com/'+u['user']['username'],'is_private':u['user']['is_private'],'is_verified':u['user']['is_verified'],'image':image_name}
            j=j+1
        else:
            user={'username':u['user']['username'],'full_name':u['user']['full_name'],'profile':'https://www.instagram.com/'+u['user']['username'],'is_private':u['user']['is_private'],'is_verified':u['user']['is_verified']}

        jsonData.append(user)
    with open(path, 'w+') as outfile:
        json.dump(jsonData, outfile)
    print("Results Instagram in: " + str(path))
    response={'results':str(path)}
    if len(users)>0:
        if knownimage:
            print("Start compare images.")
            openface_identification(knownimage,"data/instagram/"+str(now)+"_images/")
            response['images']='./data/instagram/'+str(now)+'_images/'
            response['recognized']='./data/instagram/'+str(now)+'_images/recognized/'
            if verbose:
                for r, d, f in os.walk('./data/instagram/'+str(now)+'_images/recognized/'):
                    for file in f:
                        index_json = int(file.replace("-instagram.jpg",""))
                        print("-----------")
                        print("   MATCH")
                        print("-----------")
                        print('Username: '+jsonData[index_json]['username'])
                        print('Full Name: '+jsonData[index_json]['full_name'])
                        print('Profile: https://www.instagram.com/'+jsonData[index_json]['username'])
                        print('Is Private: '+str(jsonData[index_json]['is_private']))
                        print('Is Verified: '+str(jsonData[index_json]['is_verified']))
                        print()
    return response
