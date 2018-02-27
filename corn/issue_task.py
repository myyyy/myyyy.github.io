#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import json
import urllib2
from tornado import template

def update_index():

    request = urllib2.Request("https://api.github.com/repos/myyyy/myyyy.github.io/issues")
    response = urllib2.urlopen(request)

    data = response.read()
    data = json.loads(data)
    labels = []
    for d in data:
        d['_labels'] = []
        for l in d['labels']:
            labels.append(l['name'])
            d['_labels'].append(l['name'])
    labels = list(set(labels))

    loader = template.Loader(".")
    index = loader.load("index.template").generate(data = data,labels=labels)
    with open('index.html', "w") as f:
        f.write(index)
if __name__ == '__main__':
    update_index()