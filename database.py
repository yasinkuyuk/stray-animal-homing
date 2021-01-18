import psycopg2
from classes import User,Animal,Advertisement,Advanced,Donate
import datetime
from flask import current_app

class Database:
    def __init__(self,filename):
        self.filename = filename
        self.connection = psycopg2.connect(self.filename)
        #table creations commented
        with self.connection:
            with self.connection.cursor() as cursor:
                query = """CREATE TABLE IF NOT EXISTS UserList (
                                user_id SERIAL PRIMARY KEY,
                                username VARCHAR(15) UNIQUE NOT NULL,
                                crypted_password VARCHAR(64) NOT NULL,
                                city VARCHAR(15),
                                district VARCHAR(15),
                                user_type VARCHAR(2),
                                phone_number VARCHAR(13),
                                reliability FLOAT
                            );
                            CREATE TABLE IF NOT EXISTS Animal (
                                animal_id SERIAL PRIMARY KEY,
                                age INTEGER,
                                breed VARCHAR(15) NOT NULL,
                                health_status VARCHAR(15)
                            );
                            CREATE TABLE IF NOT EXISTS Advertisement(
                                ad_id SERIAL PRIMARY KEY ,
                                user_id INTEGER NOT NULL,
                                animal_id INTEGER NOT NULL,
                                ad_date VARCHAR(10),
                                availability BOOLEAN NOT NULL,
                                FOREIGN KEY(user_id) REFERENCES UserList(user_id),
                                FOREIGN KEY(animal_id) REFERENCES Animal(animal_id)
                            );
                            CREATE TABLE IF NOT EXISTS Donation (
                                donation_id SERIAL PRIMARY KEY,
                                user_id INTEGER NOT NULL,
                                amount FLOAT NOT NULL,
                                FOREIGN KEY(user_id) REFERENCES UserList(user_id)
                            );
                            CREATE TABLE IF NOT EXISTS Vote (
                                voting_id SERIAL PRIMARY KEY,
                                voting_userID INTEGER NOT NULL,
                                voted_userID INTEGER NOT NULL,
                                vote_rate INTEGER NOT NULL,
                                FOREIGN KEY(voting_userID) REFERENCES UserList(user_id),
                                FOREIGN KEY(voted_userID) REFERENCES UserList(user_id)
                            );
                            CREATE TABLE IF NOT EXISTS Homing (
                                homing_id SERIAL PRIMARY KEY,
                                user_id INTEGER NOT NULL,
                                animal_id INTEGER NOT NULL,
                                FOREIGN KEY(user_id) REFERENCES UserList(user_id),
                                FOREIGN KEY(animal_id) REFERENCES Animal(animal_id)
                            );
                            """
                cursor.execute(query)

    def arrangeAdvertisement(self,ads):
        arrangedList = []
        for ad in ads:
            y = self.getAnimal(ad[2])
            x = Advanced(id=ad[0],username = self.getUsername(ad[1]), age=y.age, breed=y.breed, health =y.health_status, ad_date=ad[3], availability=ad[4], animalID=ad[2] )
            arrangedList.append(x)
        return arrangedList 

    def getAverageVote(self,votelist):
        counter = 0
        total = 0
        for vote in votelist:
            total += vote[0]
            counter += 1
        avg = total / counter
        return avg 

    def registerUser(self,user):
        with self.connection:
            with self.connection.cursor() as cursor:
                query = "INSERT INTO UserList (username, crypted_password, city, district, user_type, phone_number) VALUES (%s,%s,%s,%s,%s,%s)"
                cursor.execute(query, (user.username, user.password, user.city, user.district, user.userType, user.phoneNumber) )
                self.connection.commit()
        return

    def getUser(self,username):
        with self.connection:
            with self.connection.cursor() as cursor:
                query = "SELECT username, crypted_password, city, district, user_type, phone_number,reliability FROM UserList WHERE username = (%s)"
                cursor.execute(query,(username,))
                a,b,c,d,e,f,g = cursor.fetchone()
        selectedUser = User(a,b,c,d,e,f,g)
        return selectedUser

    def updateUser(self,user):
        with self.connection:
            with self.connection.cursor() as cursor:
                query = "UPDATE UserList SET crypted_password= %s, phone_number = %s, city = %s, district = %s WHERE username = (%s)"
                cursor.execute(query,(user.password ,user.phoneNumber, user.city, user.district, user.username))
                self.connection.commit()
        return

    def deleteUser(self,username):
        with self.connection:
            with self.connection.cursor() as cursor:
                cursor.execute("DELETE FROM UserList WHERE username= (%s)",(username,))
                self.connection.commit()
        return

    def getUserId(self,username):
        with self.connection:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT user_id FROM UserList WHERE username = (%s)",(username,))
                selected_user_id = cursor.fetchone()
        return selected_user_id

    def getUsername(self,id):
        with self.connection:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT username FROM UserList WHERE user_id = (%s)",(id,))
                username_ = cursor.fetchall()
        return username_

    def getAnimal(self,animal_Id):
        with self.connection:
            with self.connection.cursor() as cursor:
                query = "SELECT age,breed,health_status FROM Animal WHERE animal_id =(%s)"
                cursor.execute(query,(animal_Id,))
                animal_ = cursor.fetchall()
                animal = Animal(age = animal_[0][0], breed= animal_[0][1], health_status=animal_[0][2])
        return animal

    def createAdvertisement(self,animal,user_id_):
        with self.connection:
            with self.connection.cursor() as cursor:
                queryAnimal = "INSERT INTO Animal (age, breed, health_status) VALUES (%s,%s,%s) RETURNING animal_id"
                cursor.execute(queryAnimal,(animal.age, animal.breed, animal.health_status))
                inserted_animal_id = cursor.fetchone()[0]
                self.connection.commit()
                date = datetime.datetime.now().strftime("%x")
                query = "INSERT INTO Advertisement (user_id, animal_id, ad_date, availability) VALUES (%s,%s,%s,%s) "
                cursor.execute(query,(user_id_, inserted_animal_id, date,True))
                self.connection.commit()
        return
    

    def getAllAdvertisement(self):
        with self.connection:
            with self.connection.cursor() as cursor:
                query = "SELECT * FROM Advertisement"
                cursor.execute(query)
                ads = cursor.fetchall()
        arrangedAd = self.arrangeAdvertisement(ads)
        return arrangedAd

    def getAlluser(self):
        with self.connection:
            with self.connection.cursor() as cursor:
                query = "SELECT username, city, district, user_type, phone_number,reliability FROM UserList ORDER BY reliability DESC"
                cursor.execute(query)
                users_ = cursor.fetchall()
                users = []
                for user in users_:
                    x = User(username =user[0], password="",city=user[1], district=user[2],reliabilty=user[5], userType=user[3], phoneNumber=user[4])
                    users.append(x)
        return users

    def createDonation(self,donate):
        user_id = self.getUserId(donate.username)
        with self.connection:
            with self.connection.cursor() as cursor:
                print(donate.username)
                query = "INSERT INTO Donation (user_id, amount) VALUES (%s,%s)"
                cursor.execute(query,(user_id,donate.amount))
                self.connection.commit()
        return

    def getTotalDonation(self):
        with self.connection:
            with self.connection.cursor() as cursor:
                query = "SELECT amount FROM Donation"
                cursor.execute(query)
                amounts = cursor.fetchall()
        total = 0.0
        for amount in amounts:
            total += amount[0]
        return total
    
    def getAdvertisementByUser(self,username):
        userID = self.getUserId(username)
        with self.connection:
            with self.connection.cursor() as cursor:
                query = "SELECT * FROM Advertisement WHERE user_id = (%s)"
                cursor.execute(query,(userID,))
                ads = cursor.fetchall()
        arrangedList = self.arrangeAdvertisement(ads)
        return arrangedList

    def setVote(self,voted_username,voting_username,vote):
        voted_user_id = self.getUserId(voted_username)
        voting_user_id = self.getUserId(voting_username)
        with self.connection:
            with self.connection.cursor() as cursor:
                query = "INSERT INTO Vote (voting_userID, voted_userID, vote_rate) VALUES (%s,%s,%s)"
                cursor.execute(query,(voting_user_id,voted_user_id,vote))
                self.connection.commit()
        return

    def setUserPoint(self,username):
        userID = self.getUserId(username)
        with self.connection:
            with self.connection.cursor() as cursor:
                query = "SELECT vote_rate FROM Vote WHERE voted_userID = (%s)"
                cursor.execute(query,(userID,))
                voteList = cursor.fetchall()
        averageRate=self.getAverageVote(voteList)
        with self.connection:
            with self.connection.cursor() as cursor:
                queryUpdate = "UPDATE UserList SET reliability = %s WHERE user_id = (%s)"
                cursor.execute(queryUpdate,(averageRate,userID))
                self.connection.commit()
        return

    def getAdvertisementByBreed(self,breed):
        given_breed = breed.lower()
        ads = self.getAllAdvertisement()
        filtered = []
        for ad in ads:
            if ad.breed == given_breed:
                filtered.append(ad)
        return filtered

    def getActiveAdvertisement(self,ads):
        filtered = []
        for ad in ads:
            if ad.availability:
                filtered.append(ad)
        return filtered

    def getAdCountPerUser(self,username,selection):
        id = self.getUserId(username)
        with self.connection:
            with self.connection.cursor() as cursor:
                if selection == "active":
                    query = "SELECT COUNT(*) FROM Advertisement WHERE user_id = (%s) AND availability = (%s)"
                    cursor.execute(query,(id,True))
                else:
                    query = "SELECT COUNT(*) FROM Advertisement WHERE user_id = (%s)"
                    cursor.execute(query,(id,))
                x = cursor.fetchone()[0]
        return x
    

    def changeAddStatus(self,idA):
        with self.connection:
            with self.connection.cursor() as cursor:
                query = "UPDATE Advertisement SET availability = (%s) WHERE ad_id = (%s)"
                cursor.execute(query,(False,idA))
                self.connection.commit()
        return

    def isUser(self,username):
        with self.connection:
            with self.connection.cursor() as cursor:
                query = "SELECT EXISTS(SELECT * FROM UserList WHERE username = (%s))"
                cursor.execute(query,(username,))
                x = cursor.fetchone()[0]
        return x
    
    def getAnimalID(self,adID):
        with self.connection:
            with self.connection.cursor() as cursor:
                query = "SELECT animal_id FROM Advertisement WHERE ad_id = (%s)"
                cursor.execute(query,(adID,))
                x = cursor.fetchone()[0]
        return x

    def insertHomingObject(self,username,animalID):
        userID = self.getUserId(username)
        with self.connection:
            with self.connection.cursor() as cursor:
                query = "INSERT INTO Homing (user_id,animal_id) VALUES (%s,%s)"
                cursor.execute(query,(userID,animalID))
        return