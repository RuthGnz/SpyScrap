from peewee import *
import datetime
from playhouse.shortcuts import model_to_dict, dict_to_model
import json
import sys
from flask import jsonify
DATABASE = 'database.db'
database = SqliteDatabase(DATABASE)



# model definitions -- the standard "pattern" is to define a base model class
# that specifies which database to use.  then, any subclasses will automatically
# use the correct storage. for more information, see:
# http://charlesleifer.com/docs/peewee/peewee/models.html#model-api-smells-like-django
class BaseModel(Model):
    class Meta:
        database = database

class User(BaseModel):
    name = CharField()
    uid = CharField(unique=True)
    bio = CharField()
    birth = DateTimeField()
    gender=IntegerField()
    s_number=IntegerField()
    location = CharField()

    def getUsers():
        select=User.select()
        return (select)

    def insertUser(user_elem):
        try:
            result = (User
              .create(name=user_elem['name'],uid=user_elem['uid'], bio=user_elem['bio'], birth=user_elem['birth'],gender=user_elem['gender'],s_number=user_elem['s_number'],location=user_elem['location']))
            Photos.insertPhotos(result,user_elem['photos'])
            InstagramPhotos.insertPhotosIg(result,user_elem['instagram'])
            Schools.insertSchools(result,user_elem['schools'])
            Jobs.insertJobs(result,user_elem['jobs'])

        except IntegrityError:
            print('Couldnt insert user it might be duplicated')

    def getIds():
        result=User.select()
        response=[]
        for u in result.iterator():
            response.append(u.uid)
        return(response)

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
    
    def getByCompanyAndName(company,name):
        print(company)
        print(name)
        userIds=User.select().join(Jobs, on=(Jobs.user==User.id)).where(Jobs.job.contains(company) & User.name.contains(name))
        result = []
        for u in userIds.iterator():
            job_obj = Jobs.get(Jobs.user==u)
            json_acceptable_string = job_obj.job.replace("'", "\"")
            job = json.loads(json_acceptable_string)
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


class Photos(BaseModel):
    user=ForeignKeyField(User, backref='photos')
    photo=CharField()

    def insertPhotos(user,photos_elems):
        for p in photos_elems:
            res=Photos.insert(user=user, photo=p).execute()
    def getPhotos():
        result = []
        photos=Photos.select().join(User,on=(User.id==Photos.user)).limit(5)
        for p in photos:
            user= {'name':p.user.name,'location':p.user.location,'birth':p.user.birth}
            userData={'user':user,'photo':p.photo}
            result.append(userData)
        return result


class InstagramPhotos(BaseModel):
    user=ForeignKeyField(User, backref='inst_photos')
    photo=CharField()
    def insertPhotosIg(user,photos_elems):
        for p in photos_elems:
            InstagramPhotos.insert(user=user, photo=p).execute()

class Schools(BaseModel):
    user=ForeignKeyField(User, backref='schools')
    school=CharField()
    def insertSchools(user,schools):
        for s in schools:
            res=Schools.insert(user=user, school=s).execute()


class Jobs(BaseModel):
    user=ForeignKeyField(User, backref='jobs')
    job=CharField()
    def insertJobs(user,jobs):
        for j in jobs:
            res=Jobs.insert(user=user, job=j).execute()


class GoogleUrls():
    folder = CharField()
    photo = CharField()
    url = CharField()

def create_tables():
    with database:
        database.create_tables([User,Photos,InstagramPhotos,Schools,Jobs])




