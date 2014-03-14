# coding=utf-8

import requests


def download(url):
    resp = requests.get(url)  # TODO add retries
    return resp.content, resp.headers
