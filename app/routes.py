from app import app
from flask import render_template, request, jsonify
from server.image_captioning import image2caption
from server.txt_to_emo import preprocess, generate_emo
import base64
from datauri import DataURI

emotion = "Emotion"
story = "I will tell you a story ..."

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html", emotion=emotion, story=story)

@app.route("/", methods=["POST", "GET"])
def image2emotion():
    if request.method == "POST":
        # get image as datauri (base64 encoded string)
        img = request.form.get("img")

        # cache image as data file
        uri = DataURI(img) # parse data uri
        # uri_base64 = base64.b64decode(uri.data)  # decode from ascii bytes to base64 bytes
        img_type = uri.mimetype.split("/")[1]
        img_file = f"cached_image.{img_type}"
        with open(img_file, "wb") as fh:
            fh.write(uri.data) # write bytes to file

        # image -> emotion
        story = image2caption(img_file)
        print(f"The story is as follows:\n{story}")
        emotion = caption2emotion(story)
        print(f"The emotion is as follows:\n{emotion}")
    return jsonify({'emotion': emotion, 'story': story})

def caption2emotion(text):
    preds = preprocess(text)
    response = generate_emo(preds)
    print(f"The pre-processed text & response is:\n\t{preds}\n\t{response}")
    return response[0]
