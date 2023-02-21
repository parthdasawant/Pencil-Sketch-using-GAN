from flask import (
    Flask, render_template, request,
    redirect, url_for, session
)
from random import choice
# from tensorflow import keras
import numpy as np
import logging
import cv2
import tensorflow as tf

app = Flask(__name__)

# logging 
#logs
#--dayswise
logging.basicConfig(level=logging.DEBUG, filename="log.txt",
                    filemode="a", format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')


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


@app.route("/project.html", methods=['GET','POST'])
def cammodel():

    # image = request.form(image)
    # pred_letter  = modeltest(image)
    pred_letter='images/parth.png'
    return render_template('project.html', pred_letter=pred_letter)

@app.route("/project.htmlf", methods=['POST'])
def upmodel():

    image = request.form(image)
    pred_letter  = modeltest(image)
    return render_template('project.html' )


def modeltest(image):
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    img = cv2.resize(img,(256,256))

    img2= (img-127.5)/127.5
    img = np.reshape(img2, (-1, 256, 256, 3))
    loaded_styled_generator = tf.keras.models.load_model('C:\\Users\\PARTH\\Desktop\\rev\\saved_model\\styled_generator')

    pred_letter = loaded_styled_generator(img2, training=False)[0].numpy()
    pred_letter= (pred_letter*127.5 +127.5).astype(np.uint8)
    return pred_letter


if __name__ == "__main__":
    app.run()

