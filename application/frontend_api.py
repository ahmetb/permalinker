# coding=utf-8

import json
import os
from flask import request, jsonify, make_response
from application import webapp
from urlparse import urlparse
from os.path import splitext, basename
from datetime import datetime
from functools import wraps
import base64
from . import storage
from . import downloader
from . import api_utils

def check_auth(username, password):
    ENV_PERMUSER = os.environ['PERM_USER']
    ENV_PERMPASS = os.environ['PERM_PASS']

    """check auth"""
    return username == ENV_PERMUSER and password == ENV_PERMPASS

def authenticate():
    return make_response(
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Auth Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

@webapp.route('/api/1/upload', methods=['PUT', 'POST'])
@api_utils.crossdomain(origin='*')
@requires_auth
def api_upload():
    url = request.args.get('url')
    if not url:
        return render_api_error('URL not specified.'), 400
    try:
        filename = base64.b64encode(url)
        file_ext = get_file_ext(url)
        if file_ext:
            filename += file_ext

        start = datetime.now()

        # Download
        try:
            body, headers = downloader.download(url)
        except:
            return render_api_error('Cannot fetch file at specified URL.'), 400

        # Upload
        content_type = None if 'Content-Type' not in headers else headers[
            'Content-Type']
        permalink = storage.get_storage().upload(filename, body, content_type)
        took = (datetime.now() - start).total_seconds()
        return render_api_result({'permalink': permalink}, {'took': took}), 201
    except Exception as e:
        print e
        return render_api_error('Internal error occurred.'), 500


# File name storage utilities
def get_file_ext(url):
    path = urlparse(url).path
    if path:
        print path
        filename, file_ext = splitext(basename(path))
        return file_ext  # starts with a dot (.)


# Base API utilities
def base_api_response():
    return {}


def render_api_result(result_object, meta_object=None):
    resp = base_api_response()
    if result_object:
        resp['data'] = result_object
    if meta_object:
        resp['meta'] = meta_object
    return jsonify(**resp)


def render_api_error(error_message, error_type=None, error_code=None,
                     meta_object=None):
    error = {'message': error_message}
    if error_type:
        error['type'] = error_type
    if error_code:
        error['type'] = error_code
    resp = base_api_response()
    resp['error'] = error
    if meta_object:
        resp['meta'] = meta_object
    return jsonify(**resp)
