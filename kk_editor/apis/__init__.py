from flask_restx import Api
from apis.v0 import api as ns0

api = Api(
    title='prototype rest-api',
    version='0',
    description='중간 발표 시연을 위한 api'
)

api.add_namespace(ns0, path='/prototype')
