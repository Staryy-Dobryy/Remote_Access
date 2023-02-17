from flask import Flask, render_template, redirect, request
from wsHandler import runSocket

app = Flask("name")
runSocket()

@app.route('/')
def index():
    screen = "url(\"{{ url_for('static', filename='image.jpg') }}\");"
    return render_template("server.html", screen=screen)

@app.route('/loadImg')
def imageLoad():
    return render_template("loadImage.html")



app.run("10.0.2.15", 8080)