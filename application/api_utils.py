# coding=utf-8

from datetime import timedelta
from flask import make_response, request, current_app
from functools import update_wrapper, wraps
import os


def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator

ENV_PERMUSER = 'PERM_USER'
ENV_PERMPASS = 'PERM_PASS'


def should_check_auth():
    global ENV_PERMUSER, ENV_PERMPASS
    for k in os.environ:
        print k, '=', os.environ[k]

    return ENV_PERMUSER in os.environ and ENV_PERMPASS in os.environ


def check_auth(username, password):
    global ENV_PERMUSER, ENV_PERMPASS
    env = os.environ
    return username == env[ENV_PERMUSER] and password == env[ENV_PERMPASS]


def authenticate():
    return make_response(
        'You have to login with proper credentials', 401,
        {'WWW-Authenticate': 'Basic realm="Auth Required"'})


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        print 'should chk auth', should_check_auth()
        if auth:
            print 'is valid auth', check_auth(auth.username, auth.password)
        if should_check_auth() and (not auth or not check_auth(auth.username, auth.password)):
            return authenticate()
        return f(*args, **kwargs)
    return decorated
