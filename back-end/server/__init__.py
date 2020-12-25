from flask import Flask

app = Flask(__name__)

from server import views

app.config.from_object('config')