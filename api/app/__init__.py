from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS, cross_origin
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

cors = CORS(app)
jwt = JWTManager(app)

from app.mod_auth import routes
from app.mod_grafica import routes