from flask import Flask, render_template, redirect, request
from DBworcker import *
from wsManager import process
import websockets
import asyncio

app = Flask("name")
prepareDb("users.db")
process()

@app.route('/')
def index():
    return render_template("server.html")

@app.route('/сonnect', methods=['GET', 'POST'])
def сonnect():
    ip = request.form['connect']
    return str(ip)

app.run("127.0.0.1", 8080)