from flask import Flask, render_template, request, redirect, flash, url_for, session
import MySQLdb
import subprocess
import os

from PIL import Image
import torchvision.transforms.functional as TF
import CNN
import numpy as np
import torch
import pandas as pd
IMAGES_FOLDER = ''

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

app = Flask(__name__)
app.secret_key = "secret key"
app.config['IMAGES_FOLDER'] = IMAGES_FOLDER


@app.route('/')
@app.route("/index")
def index():
    return render_template('index.html')


@app.route("/user", methods=["GET","POST"])
def user():
    if request.method == "POST":
        db = MySQLdb.connect("localhost", "root", "", "voice_assist")
        c1 = db.cursor()
        uname = request.form["uname"]
        addr = request.form["addr"]
        city = request.form["city"]
        mno = request.form["mno"]
        emailid = request.form["emailid"]
        pwd = request.form["pwd"]

        c1.execute("INSERT INTO user VALUES ('%s','%s','%s','%s','%s','%s')" % (uname, addr, city,mno,emailid,pwd))
        db.commit()
        return render_template("user.html", msg="User Details Submitted!!!")
    return render_template("user.html")

@app.route("/userlogin", methods=["GET","POST"])
def userlogin():
    if request.method == "POST":
        db = MySQLdb.connect("localhost", "root", "", "voice_assist")
        c1 = db.cursor()
        uid=request.form["uid"]
        pwd=request.form["pwd"]


        c1.execute("select * from user where uname='%s' and pwd='%s'"%(uid,pwd))
        if c1.rowcount>=1:
            row=c1.fetchone()
            session["userid"]=uid
            return render_template("userhome.html")
        else:
            return render_template("userlogin.html", msg="Your Login attempt was not successful. Please try again!!")
    return render_template("userlogin.html")

@app.route("/userhome")
def userhome():
    return render_template('userhome.html')



@app.route("/adminlogin", methods=["GET","POST"])
def admin_login():
    if request.method == "POST":
        uid=request.form["uid"]
        pwd=request.form["pwd"]

        if uid=="admin" and pwd=="admin":
            return render_template("adminhome.html")
        else:
            return render_template("adminlogin.html", msg="Your Login attempt was not successful. Please try again!!")
    return render_template("adminlogin.html")

@app.route("/viewusers")
def viewusers():
    db = MySQLdb.connect("localhost", "root", "", "voice_assist")
    c1 = db.cursor()
    c1.execute("select * from user")
    data = c1.fetchall()
    return render_template("viewusers.html", data=data)

@app.route("/userhome1")
def userhome1():
    subprocess.run("python E:\\voice_assistant\\chatgui.py")
    return render_template("userhome2.html")

@app.route("/userhome2")
def userhome2():
    subprocess.run("python E:\\voice_assistant\\yolo.py")
    return render_template("userhome2.html")

@app.route("/index1")
def index1():
    return render_template("index1.html")

@app.route("/About_us")
def About_us():
    subprocess.run("python D:\\farmers\\alg_recom.py")
    return render_template("About_us.html")

@app.route("/analyze", methods=["GET","POST"])
def analyze():

    return render_template("analyze.html",purpose='Predicted Crop',analyzed_text=result.upper())

@app.route("/signout")
def signout():
    session.clear()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)