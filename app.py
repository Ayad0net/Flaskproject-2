from flask import Flask, redirect, request, send_file, url_for, render_template
import uuid
import u2net
from PIL import Image
import numpy as np
from matplotlib.pyplot import imread, imsave
import io
import os
import sys
import cv2
import json
app = Flask(__name__)


@app.route("/")
def home():
    message = request.args.get("message")
    return render_template("index.html", message=message)


@app.route('/upload', methods=['POST'])
def upload_file():
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        file_uuid = str(uuid.uuid1())
        uploaded_file.save("static/upload/" + file_uuid)
        return redirect("f/"+file_uuid)


@app.route("/f/<file_id>", methods=['GET'])
def process(file_id):
    img = cv2.imread("static/upload/" + file_id)

    # Process Image
    mask = u2net.run(img)  # return Image obj

    mask = np.asarray(mask)

    img = cv2.bitwise_and(img, img, mask=mask)
    #mask = cv2.bitwise_not(mask)
    # par2 is all thing not red
    # part2 = cv2.bitwise_and(img, img, mask=mask)

    imsave("static/upload/" + file_id+".png", mask)

    return send_file("static/upload/"+file_id+".png", mimetype='image/png')
    # return render_template("view.html", path='upload/'+file_id)


# app.run(debug=True)
if __name__ == '__main__':
    app.run(debug=True)
