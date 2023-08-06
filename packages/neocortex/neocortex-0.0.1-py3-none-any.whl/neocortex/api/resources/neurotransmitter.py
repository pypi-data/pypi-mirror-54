from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required


class NeurotransmitterResource(Resource):
    """Single object resource
    """
    method_decorators = [jwt_required]

    def get(self, neurotransmitter_name):
        
        return {"neurotransmitter": "{data}"}

    def put(self, neurotransmitter_name):
    
        return {"msg": "neurotransmitter updated", "neurotransmitter": "{data}"}

    def delete(self, neurotransmitter_name):
        #neurotransmitter = ""
        #neurotransmitter.delete()

        return {"msg": "neurotransmitter deleted"}


class NeurotransmitterList(Resource):
    """Creation and get_all
    """
    method_decorators = [jwt_required]

    def get(self):
        
        return {}

    def post(self):
        #request.json
        #db.session.add(user)
        #db.session.commit()

        return {"msg": "neurotransmitter created", "neurotransmitter": "data"}, 201


class NeurotransmitterFamilyByNeurotransmitter(Resource):

    method_decorators = [jwt_required]

    def get(self, neurotransmitter_name):
        return {'data':'neurotransmitter_family returned'}, 201