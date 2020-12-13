"""Flask server"""

import sys
from flask_cors import CORS
from json import dumps
from flask import Flask, request, send_from_directory
# from flask_mail import Mail, Message
from werkzeug.exceptions import HTTPException
import os

# To allow us to import from the server folder
sys.path.insert(1, os.path.join(os.path.dirname(os.path.realpath(__file__)), 
                "server"))

from add_location import add_location
from add_spaceship import add_spaceship
from update_ship_status import update_ship_status
from remove_spaceship import remove_spaceship
from remove_location import remove_location
from travel_ship import travel_ship

# To allow us to import from the server folder
sys.path.insert(1, os.path.join(os.path.dirname(os.path.realpath(__file__)), 
                "server"))

def defaultHandler(err):
    response = err.get_response()
    response.data = dumps({
        "code": err.code,
        "name": "System Error",
        "message": err.description,
    })
    response.content_type = 'application/json'
    return response



APP = Flask(__name__)
CORS(APP)

APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.register_error_handler(Exception, defaultHandler)



class ValueError(HTTPException):
    code = 400
    message = 'No message specified'


class AccessError(HTTPException):
    code = 403
    message = 'No message specified'


@APP.route('/echo', methods=['GET'])
def echo1():
    """ Description of function """
    return dumps({
        'echo' : request.args.get('echo'),
    })

@APP.route('/spaceship/add', methods=['POST'])
def add_spaceship_call():
    return dumps(add_spaceship(
        request.form.get('ship_id'),
        request.form.get('ship_name'),
        request.form.get('ship_model'),
        request.form.get('status'),
        request.form.get('location_id')
    )) + str("\n")

@APP.route('/spaceship/remove', methods=['POST'])
def remove_spaceship_call():
    return dumps(remove_spaceship(
        request.form.get('ship_id')
    )) + str("\n")

@APP.route('/spaceship/update', methods=['POST'])
def update_ship_call():
    return dumps(update_ship_status(
        request.form.get('ship_id'),
        request.form.get('status')
    )) + str("\n")

@APP.route('/location/add', methods=['POST'])
def add_location_call():
    return dumps(add_location(
        request.form.get('location_id'),
        request.form.get('city_name'),
        request.form.get('planet_name'),
        request.form.get('space_port_capacity')
    )) + str("\n")

@APP.route('/location/remove', methods=['POST'])
def remove_location_call():
    return dumps(remove_location(
        request.form.get('location_id')
    )) + str("\n")

@APP.route('/travel', methods=['POST'])
def travel_ship_call():
    return dumps(travel_ship(
        request.form.get('ship_id'),
        request.form.get('location_id')
    )) + str("\n")


if __name__ == '__main__':
    APP.run(port=(sys.argv[1] if len(sys.argv) > 1 else 5000))
