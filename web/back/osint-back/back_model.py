from peewee import *
import datetime
from playhouse.shortcuts import model_to_dict, dict_to_model
import json
import sys
from flask import jsonify
sys.path.insert(1, './CLI/')
from osint_sources.scraper import *

scriptDirectory = os.path.dirname(os.path.realpath(__file__))
print(scriptDirectory)

class User_Back(User):

    def getIds():
        result=User.select()
        response=[]
        for u in result.iterator():
            response.append(u.uid)
        return(response)

    def getById(arrayIds):
        userIds=User.select().where(User.id << arrayIds)
        result = []
        for u in userIds.iterator():
            try:
                job=Jobs.get(Jobs.user_id==u.id).job
                json_acceptable_string = job.replace("'", "\"")
                job = json.loads(json_acceptable_string)
                user= {'name':u.name,'location':u.location,'birth':u.birth,'job':job}
            except:
                print("Unexpected error:", sys.exc_info()[0])
                user= {'name':u.name,'location':u.location,'birth':u.birth,'job':''}
            photos = []
            ph = Photos.select().where(Photos.user == u)
            for i in ph.iterator():
                photos.append(i.photo)
            ig = InstagramPhotos.select().where(InstagramPhotos.user == u)
            for i in ig.iterator():
                photos.append(i.photo)
            userData={'user':user,'photos':photos}
            result.append(userData)
        return result

    def getByName(name):
        userIds=User.select().where(User.name.contains(name))
        result = []
        for u in userIds.iterator():
            try:
                job=Jobs.get(Jobs.user_id==u.id).job
                json_acceptable_string = job.replace("'", "\"")
                job = json.loads(json_acceptable_string)
                user= {'name':u.name,'location':u.location,'birth':u.birth,'job':job}
            except:
                #print("Unexpected error:", sys.exc_info()[0])
                user= {'name':u.name,'location':u.location,'birth':u.birth,'job':''}
            photos = []
            ph = Photos.select().where(Photos.user == u)
            for i in ph.iterator():
                photos.append(i.photo)
            ig = InstagramPhotos.select().where(InstagramPhotos.user == u)
            for i in ig.iterator():
                photos.append(i.photo)
            userData={'user':user,'photos':photos}
            result.append(userData)
        return result

    def getUserIdsByName(name):
        userIds=User.select().where(User.name.contains(name))
        result=[]
        for u in userIds:
            result.append(u)
        return result    

    def getByJob(company):
        userIds=Jobs.select().where(Jobs.job.contains(company))
        result = []
        for u in userIds.iterator():
            user_obj = User.get(User.id==u.user)
            json_acceptable_string = u.job.replace("'", "\"")
            job = json.loads(json_acceptable_string)
            user= {'name':user_obj.name,'location':user_obj.location,'birth':user_obj.birth,'job':job}
            photos = []
            ph = Photos.select().where(Photos.user == u.user)
            for i in ph.iterator():
                photos.append(i.photo)
            ig = InstagramPhotos.select().where(InstagramPhotos.user == u)
            for i in ig.iterator():
                photos.append(i.photo)
            userData={'user':user,'photos':photos}
            result.append(userData)

        return result

    def getUserIdsByCompany(company):
        userIds=Jobs.select().where(Jobs.job.contains(company))
        result=[]
        for u in userIds:
            result.append(u.user)
        return result
    
    def getByCompanyAndName(company,name):
        userIds=User.select().join(Jobs, on=(Jobs.user==User.id)).where(Jobs.job.contains(company) & User.name.contains(name))
        result = []
        for u in userIds.iterator():
            job_obj = Jobs.get(Jobs.user==u)

            json_acceptable_string = job_obj.job.replace("'", "\"")
            try:
                job = json.loads(json_acceptable_string)
            except:
                job=''
            user= {'name':u.name,'location':u.location,'birth':u.birth,'job':job}
            photos = []
            ph = Photos.select().where(Photos.user == u)
            for i in ph.iterator():
                photos.append(i.photo)
            ig = InstagramPhotos.select().where(InstagramPhotos.user == u)
            for i in ig.iterator():
                photos.append(i.photo)
            userData={'user':user,'photos':photos}
            result.append(userData)

        return result

    def getUsersIdsByCompanyAndName(company,name):
        userIds=User.select().join(Jobs, on=(Jobs.user==User.id)).where(Jobs.job.contains(company) & User.name.contains(name))
        result = []
        for u in userIds:
            result.append(u)
        return result

class Photos_back(Photos):
        
    def getPhotos():
        result = []
        photos=Photos.select().join(User,on=(User.id==Photos.user))
        for p in photos:
            user= {'id':p.user.id,'name':p.user.name,'location':p.user.location,'birth':p.user.birth}
            userData={'user':user,'photo':p.photo}
            result.append(userData)
        return result

    def getPhotosByUsers(users):
        result=[]
        photos=Photos.select().join(User,on=(User.id==Photos.user)).where(User.id.in_(users))
        for p in photos:
            user= {'id':p.user.id,'name':p.user.name,'location':p.user.location,'birth':p.user.birth}
            userData={'user':user,'photo':p.photo}
            result.append(userData)
        return result