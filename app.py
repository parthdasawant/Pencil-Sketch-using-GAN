import numpy as np
# from bidict import bidict
from flask import (
    Flask, render_template, request,
    redirect, url_for, session
)
from random import choice
# from tensorflow import keras
from flask import Flask, render_template, Response, request
import cv2
import datetime, time
import os, sys
import numpy as np
from threading import Thread

global capture,rec_frame, grey, switch, neg, face, rec, out 
capture=0
grey=0
neg=0
face=0
switch=1
rec=0

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about.html")
def about():
    return render_template("about.html")

@app.route("/project.html")
def project():
    return render_template("project.html")


if __name__ == "__main__":
    app.run(debug=True)
