#!/usr/bin/python
# coding=utf-8

from application import webapp
import os


if __name__ == '__main__':
    port = int(os.environ['PORT']) if 'PORT' in os.environ else None
    debug = True if not port else False
    webapp.run(host='0.0.0.0', port=port, debug=debug)
