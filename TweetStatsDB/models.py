import pymongo
import csv
from datetime import datetime
from io import StringIO


connection = pymongo.MongoClient("mongodb://localhost:27017")
#using database TMA
db = connection["ECA"]

#Insert csv file uploaded to db
def save_file(filename):
    with open(filename, 'r') as csvfile:
        #header = ["when", "who", "comment", "about", "media", "what", "whom", "refID"]
        reader = csv.reader(csvfile)
        next(reader)

        for row in reader:
            when, who, comment, about, media, what, whom, refID = row
            when = datetime.strptime(when, "%Y-%m-%d")
            create_catalog(when, who, comment, about, media, what, whom, refID)

#Collection: period
def convert_period(who, when):
    year = when.year
    month = when.month
    filter = { "who": who, "year": year, "month": month}

    cursor = db.period.find(filter)
    if cursor.count() == 0:
        filter["count"] = 1
        db.period.insert_one(filter)
    else:
        count = cursor[0]["count"]
        _id = cursor[0]["_id"]
        db.period.update({ "_id":_id }, { "$set": {"count" : count+1 }})
    return

def display_Tweetyrs(years):
    display = db.period.find_one({'year':years})
    return display

def getYearly(years):
    yearData = {}
    who = "@suss_sg"
    filter = {"who": who}
    respondC = db.period.find(filter)
    if respondC.count() != 0:
        for item in respondC:
            yearData[item["year"]] = item["count"]
    return yearData


#Collection: catalog
def create_catalog(when, who, comment, about, media, what, whom, refID):
    db.catalog.insert_one({'when':when, 'who':who, 'comment':comment, 'about':about, 'media':media, 'what':what, 'whom':whom, 'refID':refID})
    convert_period(who, when)
    return

def update_catalog(when, who, comment, about, media, what, whom, refID):
    db.catalog.update_one({'when':when, 'who':who, 'comment':comment, 'about':about, 'media':media, 'what':what, 'whom':whom, 'refID':refID})

def delete_catalog(when, who, comment, about, media, what, whom, refID):
    db.catalog.delete_one({'when':when, 'who':who, 'comment':comment, 'about':about, 'media':media, 'what':what, 'whom':whom, 'refID':refID})

#Collection: Users
def fetchUser(uid):
    print(f'User ID is {uid}')
    filter = {'uid':uid}
    result = db.users.find_one(filter)
    return result

def addUser(uid, pwd, nric):
    print(f'User ID is {uid}')
    secondFil = {'uid':uid, 'pwd':pwd, 'nric':nric}
    return db.users.insert_one(secondFil)

def updateUser(uid, newPwd):
    db.users.update_one({'uid':uid}, {'set':{'pwd':newPwd}})

def deleteUser(uid):
    db.users.delete_one({'uid':uid})