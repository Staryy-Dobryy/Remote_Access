from flask import Flask, render_template, redirect, request
from DBworcker import prepareDb
from wsManager import process, requestUsers

app = Flask("name")
prepareDb("users.db")
process()

@app.route('/')
def index():
    return render_template("client.html")

@app.route('/content')
def content():
    return render_template("load.html", users=requestUsers())

@app.route('/сonnect', methods=['GET', 'POST'])
def сonnect():
    ip = request.form['connect']
    return redirect(f"http://{ip}:8080")

app.run("127.0.0.1", 8080)