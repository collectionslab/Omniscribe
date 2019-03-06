import functools
import urllib.request
import json

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

bp = Blueprint('annnotation', __name__, url_prefix='/annotation')

def data_to_image(data,image_type):
    pass
    #TODO: convert image to readable form

@bp.route('/analyse', methods=('GET','POST'))
def analyse():
    return render_template('analyse.html')

@bp.route('/result', methods=('GET','POST'))
def result():
    uri = request.form['uri'].split(',')
    

    #TODO: call Processing AI with image
    

    
    results = [{ "image":"image1", "name":"a"},{"image":"image2", "name" :"b"}]
    return render_template('result.html',results=results ) 


