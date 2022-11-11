from flask import (
    Flask, render_template, request,
    redirect, url_for, session
)
from random import choice
# from tensorflow import keras
import numpy as np
import logging


app = Flask(__name__)

#logging for 
logging.basicConfig(level = logging.DEBUG, filename ="log.txt", filemode="a", format = "%(asctime)s - %(levelname)s - %(message)s" ) 
logger = logging.getLogger (__name__)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s' )


app = Flask(__name__)
@app.route("/")
def index():
    app.logger.info('Index.html page working')
    return render_template("index.html")

@app.route("/about.html")
def about():
    app.logger.info('about.html page working')
    return render_template("about.html")

@app.route("/project.html")
def project():
    app.logger.info('project.html page working')
    app.logger.critical('Haven\'t implemented yet')
    return render_template("project.html")


if __name__ == "__main__":
    app.run()
