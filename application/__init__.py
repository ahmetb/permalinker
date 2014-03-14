# coding=utf-8

from flask import Flask

webapp = Flask(__name__)

# creating a circular reference here however it is okay
# http://flask.pocoo.org/docs/patterns/packages/

from application import frontend_api, frontend_web
