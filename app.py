import base64
import io
import os
import PIL
from flask import (
    Flask, flash, render_template, request, send_file
)
import numpy as np
import logging
import cv2
import requests
import tensorflow as tf
from PIL import Image
import bs4
outputname="pred_letter.jpeg"
size=[]
garrey=[]
ogname=[]
ogsize=[]

# logging
logging.basicConfig(level=logging.DEBUG, filename="log.log",
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
    return render_template("project.html")


@app.route('/project.html', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        filename="input.jpeg"
        app.logger.info('Input image uploaded')
        garrey.append(filename)
        f.save(filename)
        resizeinbox(filename)
        app.logger.info('resizeinbox() is done on input image')
        img = Image.open(filename)
        data = io.BytesIO()
        img.save(data, "JPEG")
        encode_img_data = base64.b64encode(data.getvalue())
        return render_template('project.html/', filename=encode_img_data.decode("UTF-8"))

@app.route('/transform', methods=['GET', 'POST'])
def transform():
    try:
        filename=garrey.pop()
        if filename:
            app.logger.info('Input image shown into input box')
            img = Image.open(filename)
            data = io.BytesIO()
            img.save(data, "JPEG")
            encode_img_data = base64.b64encode(data.getvalue())
            image = cv2.imread(filename, cv2.COLOR_BGR2RGB)
            image = cv2.resize(image, (256, 256))
            img2 = (image-127.5)/127.5
            img = np.reshape(img2, (-1, 256, 256, 3))
            app.logger.info('input image is normalize as per model requirements')
            loaded_styled_generator = tf.keras.models.load_model(
                'C:\\Users\\PARTH\\Desktop\\saved_model\\styled_generator')#give local model path 
            app.logger.info('prediction of image done')
            pred_letter = loaded_styled_generator(img, training=False)[0].numpy()
            pred_letter = (pred_letter*127.5 + 127.5).astype(np.uint8)
            width=size.pop()
            height=size.pop()
            pred_letter = cv2.resize(pred_letter,(width,height))
            app.logger.info('resize predicted iamage as per the input iamge size')
            cv2.imwrite(outputname, pred_letter)
            img2 = Image.open(outputname)
            data = io.BytesIO()
            img2.save(data, "JPEG")
            app.logger.info('Predicted image going to output box')
            encode_img_data2 = base64.b64encode(data.getvalue())
            return render_template('project.html', filename=encode_img_data.decode(("UTF-8")), outputname=encode_img_data2.decode("UTF-8"),flag=0)
        else:
            flash('upload image or capture newone before proceeding','error')
            print('else')
    except:
        app.logger.critical('transform function failed')
        flash('upload image or capture newone before proceeding','error')

@app.route('/download')
def download_file():
	#path = "html2pdf.pdf"
	#path = "info.xlsx"
	path = "pred_letter.jpeg"
	#path = "sample.txt"
	return send_file(path, as_attachment=True)


def resizeinbox(filename):
    fixed_size = 400
    image = Image.open(filename)
    if float(image.size[1])<400 and float(image.size[0])<400:
        size.append(image.size[1])
        size.append(image.size[0])
        app.logger.info('given image dim < 400') 
    elif float(image.size[1])>float(image.size[0]):
        height_percent = (fixed_size / float(image.size[1]))
        width_size = int((float(image.size[0]) * float(height_percent)))
        image = image.resize((width_size, fixed_size), PIL.Image.NEAREST)
        image.save(filename)
        size.append(fixed_size)
        size.append(width_size) 
        app.logger.info('given image is potrait')
    else:
        height_percent = (fixed_size / float(image.size[0]))
        width_size = int((float(image.size[1]) * float(height_percent)))
        image = image.resize((fixed_size, width_size), PIL.Image.NEAREST)
        image.save(filename)
        size.append(width_size) 
        size.append(fixed_size)
        app.logger.info('given image is landscape')
    app.logger.info('given image gone through resizeinbox()')


if __name__ == "__main__":
    app.secret_key='super secret key'
    app.config['SESSION_TYPE']='filesystem'
    port = int(os.environ.get('PORT',5000))
    app.run(host='0.0.0.0', port=port)
