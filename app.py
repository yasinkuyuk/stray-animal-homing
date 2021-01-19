from database import Database
from flask import Flask, render_template,flash,redirect,url_for,current_app
from datetime import datetime
from forms import RegistationForm, LoginForm, AdvertisementForm, hashPassword, updateUserInformation, VoteForm, DonationForm, SearchAdvertisementForm,Homing
from classes import User,Animal,Donate

POSTGRESQL_URI = "postgres://xvkkgnpe:EMnqE0mIThM4GFRail4rkLJF0tKRXUAT@rogue.db.elephantsql.com:5432/xvkkgnpe"
db = Database(POSTGRESQL_URI)
current_user = User("","")

app = Flask(__name__)
app.config["SECRET_KEY"] = "b2e0242696bacbe7cf12d8a4b739b021"
app.config["db"] = db
app.config["isValidUser"] = False
app.config["current_user"] = current_user

@app.route("/")
def home_page():
    return render_template("home.html",user_validation=current_app.config["isValidUser"],username = current_app.config["current_user"].username)

@app.route("/user", methods=["GET","POST"])
def user_page():
    voteform = VoteForm()
    users = db.getAlluser()
    cur_username = current_app.config["current_user"].username
    for user in users:
        if user.username != cur_username:
            voteform.username.choices.append(user.username)

    if voteform.validate_on_submit():
        flash(f"Congrats! You've voted {voteform.vote.data}/10 for {voteform.username.data}! ",'success')
        voted_username = voteform.username.data
        vote = voteform.vote.data
        db.setVote(voted_username,cur_username,vote)
        db.setUserPoint(voted_username)
        return redirect(url_for('user_page'))

    return render_template("user.html",user_validation = current_app.config["isValidUser"] , username = current_app.config["current_user"].username, users=users,form =voteform)

@app.route("/donation", methods=["GET","POST"])
def donation_page():
    form = DonationForm()
    x = db.getTotalDonation()
    if form.validate_on_submit():
        flash(f"Thank you for donating {form.amount.data} Turkish Liras",'success')
        donation_form = Donate(amount=form.amount.data, username=current_app.config["current_user"].username)
        db.createDonation(donation_form)
        return redirect(url_for('donation_page'))
    return render_template("donation.html",user_validation=current_app.config["isValidUser"],username = current_app.config["current_user"].username,form=form,x=x)

@app.route("/ad",methods=["GET","POST"])
def ad_page():
    form = SearchAdvertisementForm()
    ads = db.getAllAdvertisement()
    ads = db.getActiveAdvertisement(ads)
    if form.validate_on_submit():
        breed = form.breed.data
        ads = db.getAdvertisementByBreed(breed)
        return render_template("ad.html",user_validation=current_app.config["isValidUser"],username = current_app.config["current_user"].username, ads=ads,form = form)

    return render_template("ad.html",user_validation=current_app.config["isValidUser"],username = current_app.config["current_user"].username, ads=ads,form = form)

@app.route("/register",methods=["GET","POST"])
def register_page():
    form = RegistationForm()
    if form.validate_on_submit():
        if not db.isUser(form.username.data):     
            flash(f'Account created for {form.username.data}! You are now able to log in', 'success')
            user = User(form.username.data, form.password.data, form.city.data, form.district.data, 0.0, form.userType.data, form.phoneNumber.data)
            hashedPassword = hashPassword(user.password)
            user.password = hashedPassword
            db.registerUser(user)
            return redirect(url_for('login_page'))
        else:
            flash(f'This username exists. Please pick another username.', 'danger')
            return redirect(url_for("register_page"))
    return render_template("register.html", title = "Register", form = form)

@app.route("/login",methods = ["GET","POST"])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        user = User(username = form.username.data,password=form.password.data)
        hashedPassword = hashPassword(user.password)
        user_ = db.getUser(user.username)
        if hashedPassword == user_.password:
            flash(f'Welcome {user.username}!', 'success')
            current_app.config["current_user"] = user_
            current_app.config["isValidUser"] = True
            return redirect(url_for("home_page"))
        else:
            flash(f'Wrong pasword, please try again!', 'danger')
            return redirect(url_for("login_page"))

    return render_template("login.html", title = "Login", form=form)

@app.route("/logout")
def logout_page():
    user=User(username="",password="")
    current_app.config["current_user"]=user
    current_app.config["isValidUser"] = False
    return redirect(url_for("home_page"))

@app.route("/myProfile",methods=["GET", "POST"])
def profile_page():
    adForm = AdvertisementForm()
    upForm = updateUserInformation()
    homForm = Homing()
    users = db.getAlluser()
    ads = db.getAdvertisementByUser(current_app.config["current_user"].username)
    active = db.getAdCountPerUser(current_app.config["current_user"].username, "active")
    total = db.getAdCountPerUser( current_app.config["current_user"].username, "total")

    for user in users:
        homForm.username.choices.append(user.username)

    for ad in ads:
        homForm.ad_id.choices.append(ad.id)

    if homForm.validate_on_submit():
        flash(f'Advertisment removed from the public advertisment list', "success")
        adID = homForm.ad_id.data
        animalID = db.getAnimalID(adID)
        db.insertHomingObject(homForm.username.data,animalID)
        db.changeAddStatus(adID)
        return redirect(url_for("profile_page"))

    if adForm.validate_on_submit():
        flash(f'Advertisement created!', 'success')
        animal = Animal(age = adForm.age.data, breed = adForm.breed.data, health_status=adForm.health_status.data)
        user_id_ = db.getUserId(current_app.config["current_user"].username)
        db.createAdvertisement(animal,user_id_)
        return redirect(url_for("ad_page"))
    
    if upForm.validate_on_submit():
        flash(f'User informations updated!', 'success')
        username = current_app.config["current_user"].username
        password = current_app.config["current_user"].password
        city = current_app.config["current_user"].city
        district = current_app.config["current_user"].district
        phone = current_app.config["current_user"].phoneNumber
        user_type = current_app.config["current_user"].userType
        
        if upForm.password.data != "":
            password = hashPassword(upForm.password.data)
        
        if upForm.phoneNumber.data != "":
            phone = upForm.phoneNumber.data
        
        if upForm.city.data != "":
            city = upForm.city.data
        
        if upForm.district.data != "":
            district = upForm.district.data

        if upForm.userType.data != "":
            user_type = upForm.userType.data

        user = User(username,password=password,city = city, district=district, phoneNumber=phone, userType=user_type)
        db.updateUser(user)
        return redirect(url_for("profile_page"))
    if current_app.config["isValidUser"]:
        return render_template("myprofile.html",form=adForm, upForm=upForm, user_validation=current_app.config["isValidUser"],username = current_app.config["current_user"].username,myAds = ads,total=total,activeNumber = active,hform = homForm)
    else:
        flash(f'Please log in to use this feature')
        return redirect(url_for("login_page"))

@app.route("/del",methods=["GET","POST"])
def delete_user():
    db.deleteUser( current_app.config["current_user"].username )
    user=User(username="",password="")
    flash(f'Account deleted for {current_app.config["current_user"].username}!', 'success')
    current_app.config["current_user"]=user
    current_app.config["isValidUser"] = False
    return redirect(url_for("home_page"))
   


if __name__ == "__main__":
    app.run(host = "0.0.0.0", port =8080, debug=True)
