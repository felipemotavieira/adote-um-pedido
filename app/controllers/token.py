from flask_restplus import Resource
from instance import server
api = server.api
from models.pix import PixModel

@api.route('/token', methods=['POST'])
class Token(Resource):
    def post(self):
        pix_model = PixModel()
        response = pix_model.get_token()
        return response