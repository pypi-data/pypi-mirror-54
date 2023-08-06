# -*- coding: utf-8 -*-
"""
Created on Fri Oct 26 00:06:43 2019

@author: Tyler

DEPRECATED
May return to build later
"""

import requests
import json
import logging
import neocortex.api.urls as URLS

class _neurotransmitter:
    def __init__(self, client, neurotransmitter_name):
        self._client = client
        self.neurotransmitter_name = neurotransmitter_name

    def create(self):
        return

    def get_data(self):
        url = URLS.api_prefix + URLS.neurotransmitter + '/' + self.neurotransmitter_name
        return self._client._get(url)

    def update(self):
        return

    def get_family(self):
        url = URLS.api_prefix + URLS.neurotransmitter + '/' + self.neurotransmitter_name + URLS.neurotransmitterfamily
        return self._client._get(url)

class NeoClient:

    def __init__(self, user, password, server="127.0.0.1", port="", schema='http://'):
        self._user = user
        self._password = password
        self._server = server 
        if port:
            self._server = self._server + ":" + port
        self._schema = schema
        self._token = None

        return
    
    def _auth(self, connect_timeout=5.0, read_timeout=300.0):
        url = self._schema + self._server + URLS.auth_prefix + URLS.auth_login

        payload = {"username": self._user, "password": self._password}
        r = requests.post(url, json=payload, timeout=(connect_timeout, read_timeout))
        json_data = r.json()
        token = json_data.get("access_token")
        return token

    def _post(self, entry, payload):
        url = self._schema + self._server + entry
        token = self._auth()
        headers = {"Authorization":"Bearer " + token,"Content-Type":"application/json"}    
        connect_timeout, read_timeout = 5.0, 300.0
        r = requests.post(url, data=json.dumps(payload), headers=headers,timeout=(connect_timeout, read_timeout))
        return r

    def _get(self, entry, params = {}):
        url = self._schema + self._server + entry
        token = self._auth()
        headers = {"Authorization":"Bearer " + token,"Content-Type":"application/json"}    
        connect_timeout, read_timeout = 5.0, 300.0
        r = requests.get(url=url, params=params, headers=headers, timeout=(connect_timeout, read_timeout))
        return r

    def neurotransmitter(self, neurotransmitter_name):
        return _neurotransmitter(self, neurotransmitter_name)

    def query(self, q):
        url_query = URLS.api_prefix + URLS.raw_query

        if q:
            payload = {
                    "query":q
                    }
            ret= self._post(url_query,payload)
            retjson =  json.loads(ret.text)
            return retjson

        else:
            return None
