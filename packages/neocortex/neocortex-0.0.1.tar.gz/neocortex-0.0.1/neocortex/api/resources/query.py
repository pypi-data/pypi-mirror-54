# -*- coding: utf-8 -*-
"""
Created on Tue Nov 20 19:37:51 2018

@author: Tyler
"""

from flask_restful import Resource
from flask_jwt_extended import jwt_required

from webargs import fields, validate
from webargs.flaskparser import use_args, use_kwargs, parser, abort

from neocortex.extensions import neo4j

class RawQuery(Resource):
    """List object resource
    """
    method_decorators = [jwt_required]
   
    query_args = {
    'query': fields.Str(required=True)
    }
   
    @use_args(query_args)
    def post(self, args):
        return neo4j.gdb.run(args["query"]).data(), 200