#!/usr/bin/env python3

##
## Sample Flask REST server implementing two methods
##
## Endpoint /api/image is a POST method taking a body containing an image
## It returns a JSON document providing the 'width' and 'height' of the
## image that was provided. The Python Image Library (pillow) is used to
## process the image
##
## Endpoint /api/add/X/Y is a post or get method returns a JSON body
## containing the sum of 'X' and 'Y'. The body of the request is ignored
##
##
from flask import Flask, request, Response
import jsonpickle
from PIL import Image
import base64
import io
import json
import numpy as np

# Initialize the Flask application
app = Flask(__name__)

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.DEBUG)

@app.route('/api/add/<int:a>/<int:b>', methods=['GET', 'POST'])
def add(a,b):
    response = {'sum' : str( a + b)}
    response_pickled = jsonpickle.encode(response)
    return Response(response=response_pickled, status=200, mimetype="application/json")

# route http posts to this method
@app.route('/api/rawimage', methods=['POST'])
def rawimage():
    r = request
    # convert the data to a PIL image type so we can extract dimensions
    try:
        ioBuffer = io.BytesIO(r.data)
        img = Image.open(ioBuffer)
    # build a response dict to send back to client
        response = {
            'width' : img.size[0],
            'height' : img.size[1]
            }
    except:
        response = { 'width' : 0, 'height' : 0}
    # encode response using jsonpickle
    response_pickled = jsonpickle.encode(response)

    return Response(response=response_pickled, status=200, mimetype="application/json")

# route http posts to this method
@app.route('/api/dotproduct', methods=['POST'])
def dotproduct():
    try:
        # Parse the request JSON to extract vectors 'a' and 'b'
        data = request.get_json()
        a = np.array(data['a'])
        b = np.array(data['b'])

        # Calculate the dot product
        dot_product = np.dot(a, b)

        # Build a response dict with the result
        response = {'dot_product': float(dot_product)}
    except Exception as e:
        # In case of an error, return a default response
        response = {'error': str(e)}
    
    # Encode response using jsonpickle
    response_pickled = jsonpickle.encode(response)
    return Response(response=response_pickled, status=200, mimetype="application/json")

# route http posts to this method
@app.route('/api/jsonimage', methods=['POST'])
def jsonimage():
    try:
        # Parse the request JSON to extract the base64 encoded image
        data = request.get_json()
        img_data = base64.b64decode(data['image'])

        # Convert the base64 decoded data to a PIL Image
        ioBuffer = io.BytesIO(img_data)
        img = Image.open(ioBuffer)

        # Build a response dict with the image dimensions
        response = {
            'width': img.size[0],
            'height': img.size[1]
        }
    except Exception as e:
        # In case of an error, return a default response
        response = {'width': 0, 'height': 0, 'error': str(e)}
    
    # Encode response using jsonpickle
    response_pickled = jsonpickle.encode(response)
    return Response(response=response_pickled, status=200, mimetype="application/json")

# start flask app
app.run(host="0.0.0.0", port=5000)
