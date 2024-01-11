from flask import Flask, request, render_template, Response
from requests import request

app = Flask(__name__)

@app.route("/auth", methods=['GET'])
