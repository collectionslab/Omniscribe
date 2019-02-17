import functools
import urllib.request
import json

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

bp = Blueprint('annnotation', __name__, url_prefix='/annotation')

def data_to_image(data,image_type):
    #TODO: convert image to readable form

@bp.route('/analyse', methods=(GET))
def analyse():
    return render_template('analyse.html')

@bp.route('/result', methods=(GET))
def result():
    uri = request.form['uri']
    try:
        response = urllib.request.urlopen(uri)
    except:
        abort(404)

    content_type = response.getheader("Content-Type").split(';')
    mime_type = content_type[0].split['/']
    images = []
    if mime_type[0] == image:
        img = data_to_image(response.read(),mime_type[1])
        images.append(img)
    
    else if mime_type[0] == "application" && mime_type[1] == "json"
        response_js = json.loads(response.read())
        for sequence in response_js["sequences"]:
            for canvas in sequence["canvases"]:
                for image in canvas["images"]:
                    image_uri = image["resource"]["@id"]
                    image_type = image["resource"]["format"].split('/')[1]
                    response = urllib.request.urlopen(image_uri)
                    img = data_to_image(response.read(),image_type)
                    images.append(img)
    else
        abort(404)

    #TODO: call Processing AI with image
    
    return render_template('result.html') 


