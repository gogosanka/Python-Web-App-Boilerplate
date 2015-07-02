from flask import Blueprint

main = Blueprint('main',__name__)


from smh.views import *
from smh.errors import *
