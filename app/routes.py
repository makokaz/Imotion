from app import app
from flask import render_template, request
from server.image_captioning import image2caption
from server.txt_to_emo import preprocess, generate_emo

emotion = "Emotion"
story = "I will tell you a story ..."

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html", emotion=emotion, story=story)

@app.route("/", methods=["POST", "GET"])
def image2emotion():
    if request.method == "POST":
        img = request.form.get("img")
        last_position = find_last(img, "\\") # you may change this dependending on the path style on you pc
        img_file = "./image" + img[last_position:]
        story = image2caption(img_file)
        emotion = txt_to_emo(story)
    return render_template("index.html", emotion=emotion, story=story)

@app.route('/img', methods=["POST", "GET"])
def home():
    if request.method == "POST":
        img = request.form.get("img")
        print(img)
    return render_template("index.html")

def txt_to_emo(text):
    preds = preprocess(text)
    response = generate_emo(preds)
    return response[0]

def find_last(string,str):
    last_position=-1
    while True:
        position=string.find(str,last_position+1)
        if position==-1:
            return last_position
        last_position=position