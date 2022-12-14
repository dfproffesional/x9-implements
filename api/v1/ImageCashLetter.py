from flask import (
  Blueprint,
  jsonify
)
from time import time
from config import default_json_response

bp = Blueprint('icl', __name__, url_prefix="/api/v1/icl")

@bp.route('/')
def index():
  # init time
  i = time()
  # get response
  return default_json_response({
    'data': [],
    'status': 400,
    'message': 'ok',
    'duration':time() - i
  })