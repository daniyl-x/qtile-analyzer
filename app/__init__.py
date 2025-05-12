import os
from dotenv import load_dotenv

from flask import Flask

from app import db
from app.routes.api import api


load_dotenv()

app = Flask(__name__)
app.config["DATABASE"] = os.path.join(app.instance_path, os.getenv("DATABASE"))
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

try:
    os.makedirs(app.instance_path)
except OSError:
    pass

db.init_app(app)

app.register_blueprint(api, url_prefix="/api")
