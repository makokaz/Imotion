from app import app
from flask import render_template, jsonify, request
from server.image_captioning import image2caption
from server.txt_to_emo import preprocess, generate_emo
import sys

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")

@app.route('/img', methods=["POST", "GET"])
def home():
    if request.method == "POST":
        img = request.form.get("img")
        print(img)
    return render_template("index.html")

@app.route('/res', methods=['GET'])
def txt_to_emo():
    text = image2caption('./server/img2.jpg')
    print(text)
    preds = preprocess(text)
    response = generate_emo(preds)
    return jsonify(result=response)

