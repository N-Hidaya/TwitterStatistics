from flask import Flask, render_template, request, jsonify, session
from bson import json_util
import models
import json

app = Flask(__name__)
app.secret_key = "pleaseB3K1nd"


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "GET":
        return render_template("index.html")
    
    elif request.method == "POST":
        userEmail = request.form.get("email")
        userPwd = request.form.get("password")
        print(f"Login: Email is {userEmail} and Password id {userPwd}")

        if(userEmail != "" and userPwd != ""):
            session["username"] = userEmail
            return render_template("catalog.html")
        else:
            return "Wrong Account!"

@app.route("/logout")
def logout():
    if "username" in session:
        aEmail = session["username"]
        print(f"Logout: session {aEmail}")
        session.pop("username", None)

    return render_template("index.html")

@app.route("/upload", methods=["GET", "POST"])
@app.route("/upload/<path:filename>", methods=["POST"])
def upload():
    if request.method == "GET":
        return render_template("upload.html")
    elif request.method == "POST":
        filename = request.form.get("filename")
        #save to db
        models.save_file(filename)
        
        return render_template("upload.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    elif request.method == "POST":
        userEmail = request.form.get("email")
        userPwd = request.form.get("password")
        nric = request.form.get("nric")

        print(f"Register: Email is {userEmail}, Password is {userPwd}, NRIC is {nric}")

        return render_template("index.html")

@app.route("/catalog", methods=["GET", "POST"])
def catalog():
    if request.method == "GET":
        return render_template("catalog.html")
    elif request.method == "POST":
        when = request.form.get("when")
        who = request.form.get("who")
        comment = request.form.get("comment")
        about = request.form.get("about")
        media = request.form.get("media")
        what = request.form.get("what")
        whom = request.form.get("whom")
        refID = request.form.get("refID")

        print(f"When: {when}, Who: {who}, Comment: {comment}, About: {about}, Media: {media}, What: {what}, Whom: {whom}, ReferenceID: {refID}")

        #To insert catalog details in MongoDB
        models.create_catalog(when,who,comment,about,media,what,whom,refID)
        catalogData = [when, who, comment, about, media, what, whom, refID]
        return jsonify({"catalogData":catalogData})

        #to fetch number of tweets by year
        #tweetsByYear = models.read_date()

        #return jsonify({"catalogData":catalogData, "tweetsByYear":tweetsByYear})

@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if request.method == "GET":
        labelyrs = ["All", 2013,2014,2015,2016,2017,2018,2019,2020,2021]
        return render_template("dashboard.html", yroptions=labelyrs)

    elif request.method == "POST":
        labelyrs = [2013,2014,2015,2016,2017,2018,2019,2020,2021]
        months = []
        tweetCount = []
        for yrs in labelyrs:
            fields = models.display_Tweetyrs(yrs)
            month = fields["month"]
            count = fields["count"]
            months.append(month)
            tweetCount.append(count)
  
            print(f'{fields}')


        return jsonify({"months":months,"tweets":tweetCount})
