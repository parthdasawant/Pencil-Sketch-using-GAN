import numpy as np
# from bidict import bidict
from flask import (
    Flask, render_template, request,
    redirect, url_for, session
)
from random import choice
# from tensorflow import keras


app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
