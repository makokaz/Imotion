from app import app
from flask import render_template
from server.image_captioning import caption

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html", title=caption("Imotion"))