from peewee import *
import datetime
DATABASE = './data/database.db'
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

class Photos(BaseModel):
    user=ForeignKeyField(User, backref='photos')
    photo=CharField()

    def insertPhotos(user,photos_elems):
        for p in photos_elems:
            res=Photos.insert(user=user, photo=p).execute()



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




