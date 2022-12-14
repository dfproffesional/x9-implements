import os
from flask import Flask, Response
from dotenv import load_dotenv

load_dotenv()
def set_config_app(app:Flask)-> None:
  if (os.getenv('ENV')!="production"):
    app.config.update(
      TESTING=True,
      ENV="development",
      DEBUG=True,
      PROPAGATE_EXCEPTIONS=True,
    )
  else:
    app.config.update(
      TESTING=False,
      ENV="production",
      DEBUG=False,
      PROPAGATE_EXCEPTIONS=False,
      HOST='0.0.0.0',
      PORT=80
    )

def default_json_response(dict:dict)->Response:
  from flask import jsonify

  response = {
    'data' : dict['data'],
    'message' : dict['message'],
    'duration' : dict['duration'],
    'duraton_unit' : 'seg'
  }
  if 'error' in dict.keys():
    response['error'] = dict['error']

  get_json = jsonify(response)
  get_json.status_code = dict['status']
  return get_json