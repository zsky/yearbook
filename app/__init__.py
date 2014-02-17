#encoding: utf-8
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

import sys
reload(sys)
sys.setdefaultencoding('utf8')

from app import views, models

