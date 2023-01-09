from flask import request
from flask_restplus import Resource
from models.pix import PixModel
from instance import server

api = server.api

@api.routes('/orders', methods='POST')
class Pix(Resource):
    def post(self,):
        payload = request.json
        #!! pop
        txid = payload.pop('txid')

        pix_model = PixModel
        response = pix_model.create_charge(txid, payload)

        return response

