from app import app
from flask import render_template, request
from server.image_captioning import image2caption
from server.txt_to_emo import preprocess, generate_emo

emotion = "Emotion"
story = "I will tell you a story ..."

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html", title="Imotion", emotion=emotion, story=story)

@app.route("/", methods=["POST", "GET"])
def image2emotion():
    if request.method == "POST":
        img = request.form.get("img")
        print(img)
        # img_caption = image2caption(img)
        # emotion = txt_to_emo(img_caption)
        # TODO: Put caption to emotion-box in index.html
        # emotion = img
    return render_template("index.html", title="Imotion", emotion=emotion, story=story)

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
