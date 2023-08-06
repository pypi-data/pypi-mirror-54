from flask import Blueprint
from flask_restful import Api

from neocortex.api.resources.query import RawQuery
from neocortex.api.resources.user import UserResource, UserList
from neocortex.api.resources.neurotransmitter import NeurotransmitterResource, NeurotransmitterList, NeurotransmitterFamilyByNeurotransmitter
from neocortex.api import urls as URLS

blueprint_one = Blueprint('api', __name__, url_prefix=URLS.api_prefix)
api_one = Api(blueprint_one)

api_one.add_resource(RawQuery, URLS.raw_query)
api_one.add_resource(UserResource, URLS.users + '/<int:user_id>')
api_one.add_resource(UserList, URLS.users)

api_one.add_resource(NeurotransmitterResource, URLS.neurotransmitter + '/<string:neurotransmitter_name>')
api_one.add_resource(NeurotransmitterList, URLS.neurotransmitter)
api_one.add_resource(NeurotransmitterFamilyByNeurotransmitter, 
                    URLS.neurotransmitter + '/<string:neurotransmitter_name>'+ URLS.neurotransmitterfamily)  