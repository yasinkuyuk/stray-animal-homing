import os
from flask import Flask, render_template
from classes import User
import view
from database import Database

POSTGRESQL_URI = "postgres://xvkkgnpe:EMnqE0mIThM4GFRail4rkLJF0tKRXUAT@rogue.db.elephantsql.com:5432/xvkkgnpe"
db = Database(POSTGRESQL_URI)

current_user = User("","")

app = Flask(__name__)
app.add_url_rule("/", view_func = view.home_page)
app.add_url_rule("/ad", view_func = view.ad_page, methods = ["GET","POST"])
app.add_url_rule("/user", view_func = view.user_page, methods = ["GET","POST"])
app.add_url_rule("/donation", view_func = view.donation_page, methods=["GET","POST"])
app.add_url_rule("/register", view_func = view.register_page,methods = ["GET","POST"])
app.add_url_rule("/login", view_func = view.login_page, methods = ["GET","POST"])
app.add_url_rule("/logout", view_func = view.logout_page)
app.add_url_rule("/myProfile",view_func=view.profile_page, methods = ["GET","POST"])
app.add_url_rule("/del",view_func = view.delete_user)
app.config["SECRET_KEY"] = "b2e0242696bacbe7cf12d8a4b739b021"

if __name__ == "__main__":
    app.config["db"] = db
    app.config["isValidUser"] = False
    app.config["current_user"] = current_user
    app.run(host = "0.0.0.0", port =8080, debug=True)
