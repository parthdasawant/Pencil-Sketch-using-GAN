import base64
import io
from flask import (
    Flask, flash, render_template, request,
    redirect, url_for, session
)
from random import choice
# from tensorflow import keras
import numpy as np
import logging
import cv2
import tensorflow as tf
from PIL import Image
from werkzeug.utils import secure_filename
gfilename=""
outputname="pred_letter.jpeg"
app = Flask(__name__)

# logging
logging.basicConfig(level=logging.DEBUG, filename="log.txt",
                    filemode="a", format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

app.config["IMAGE_UPLOADS"]="C:\\Users\\PARTH\\Pencil-Sketch-using-GAN\\static\\images"


garrey=[]

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


@app.route('/project.html', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        # image = f
        # filename= secure_filename(f.filename)
        filename="input.jpeg"
        garrey.append(filename)
        f.save(filename)
        image = cv2.imread(filename, cv2.COLOR_BGR2RGB)
        image = cv2.resize(image, (400, 400))
        cv2.imwrite(filename,image)
        img = Image.open(filename)
        data = io.BytesIO()
        img.save(data, "JPEG")
        encode_img_data = base64.b64encode(data.getvalue())
        print(f)
        return render_template('project.html/', filename=encode_img_data.decode("UTF-8"))
    
@app.route('/transform', methods=['GET', 'POST'])
def transform():
    try:
        filename=garrey.pop()
        if filename:
            img = Image.open(filename)
            data = io.BytesIO()
            img.save(data, "JPEG")
            encode_img_data = base64.b64encode(data.getvalue())
            image = cv2.imread(filename, cv2.COLOR_BGR2RGB)
                # modeltest(image)

            image = cv2.resize(image, (256, 256))
            img2 = (image-127.5)/127.5
            img = np.reshape(img2, (-1, 256, 256, 3))
            loaded_styled_generator = tf.keras.models.load_model(
                'C:\\Users\\PARTH\\Desktop\\saved_model\\styled_generator')

            pred_letter = loaded_styled_generator(img, training=False)[0].numpy()
            pred_letter = (pred_letter*127.5 + 127.5).astype(np.uint8)
            pred_letter = cv2.resize(pred_letter,(400,400))
            cv2.imwrite(outputname, pred_letter)
            img2 = Image.open(outputname)
            data = io.BytesIO()
            img2.save(data, "JPEG")
            encode_img_data2 = base64.b64encode(data.getvalue())
            return render_template('project.html', filename=encode_img_data.decode(("UTF-8")), outputname=encode_img_data2.decode("UTF-8"))
        else:
            flash('upload image or capture newone before proceeding','error')
            print('else')
    except:
        flash('upload image or capture newone before proceeding','error')

def modeltest(image):
    # img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    img = cv2.resize(image, (256, 256))

    img2 = (img-127.5)/127.5
    img = np.reshape(img2, (-1, 256, 256, 3))
    loaded_styled_generator = tf.keras.models.load_model(
        'C:\\Users\\PARTH\\Desktop\\rev\\saved_model\\styled_generator')

    pred_letter = loaded_styled_generator(img2, training=False)[0].numpy()
    pred_letter = (pred_letter*127.5 + 127.5).astype(np.uint8)
    pred_letter.save('output.jpg')
    return 'sucsess'


if __name__ == "__main__":
    app.secret_key='super secret key'
    app.config['SESSION_TYPE']='filesystem'
    app.run(debug=True)
