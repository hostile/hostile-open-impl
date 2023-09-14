import os

from flask import Flask

from ghunt_blueprint import blueprint as ghunt_blueprint
from holehe_blueprint import blueprint as holehe_blueprint

app = Flask(__name__)

app.register_blueprint(ghunt_blueprint)
app.register_blueprint(holehe_blueprint)

def run():
    app.run(host=os.getenv('HOST'), port=os.getenv('PORT'))