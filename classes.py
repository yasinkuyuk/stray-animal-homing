class User:
    def __init__(self,username,password,city = None, district = None, reliabilty = None, userType = None, phoneNumber = None):
        self.username = username
        self.password = password
        self.city = city
        self.district = district
        self.reliability = reliabilty
        self.userType = userType
        self.phoneNumber = phoneNumber
        
class Advanced:
    def __init__(self,id,username,age,breed,health,ad_date,availability,animalID):
        self.id = id
        self.username = username
        self.age = age
        self.breed = breed
        self.health = health
        self.ad_date = ad_date
        self.availability = availability
        self.animalID = animalID
        
class Animal:
    def __init__(self,age,breed,health_status):
        self.age = age
        self.breed = breed
        self.health_status = health_status

class Advertisement:
    def __init__(self,ad_id,user_id,animal_id,date,activeness):
        self.ad_id = ad_id
        self.animal_id = animal_id
        self.user_id = user_id
        self.date = date
        self.activeness = activeness

class Voting:
    def __init__(self,vote_id,voting_user_id, voted_user_id,vote):
        self.vote_id = vote_id
        self.voting_user_id = voting_user_id
        self.voted_user_id = voted_user_id
        self.vote = vote

class Homing:
    def __init__(self,homing_id,user_id,animal_id):
        self.homing_id = homing_id
        self.user_id = user_id
        self.animal_id = animal_id

class Donate:
    def __init__(self,amount,username):
        self.amount = amount
        self.username = username