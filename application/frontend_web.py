# coding=utf-8


from application import webapp
from flask import make_response


@webapp.route('/')
def index():
    motd = 'Permalinker server active!\nNow configure the browser extension.'
    resp = make_response(motd)
    resp.headers['Content-Type'] = 'text/plain'
    return resp
