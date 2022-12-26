from flask import (
  Blueprint,
  request
)
from time import time
from config import default_json_response
from modules.ImageCashLetter import Read

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

@bp.route('/read',methods=["POST"])
def read():
  try:
    if not request.is_json:
      raise Exception("Bad request")
    # init time
    i = time()
    # get icl 
    get_data = Read.read_json(request.get_json())
    # get response
    return default_json_response({
      'data': get_data,
      'status': 200,
      'message': 'ok',
      'duration':time() - i
    })
  except Exception as err:
    return default_json_response({
      'data': None,
      'status': 400,
      'message': str(err),
      'duration':time() - i
    })