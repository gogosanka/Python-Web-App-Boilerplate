from flask import Blueprint

auth = Blueprint('auth',__name__)

from smh.views import *