#from typing_extensions import Required
from flask_restful import Resource, reqparse
from models.hotel import HotelModel
 
hoteis = [
    {
        'hotel_id': 'alpha',
        'nome': 'Alpha hotel',
        'estrelas': '4.3',
        'diaria': '420.34',
        'cidade': 'Rio de Janeiro'
    },
    {
        'hotel_id': 'bravo',
        'nome': 'Bravo hotel',
        'estrelas': '4.4',
        'diaria': '380.90',
        'cidade': 'Santa Catarina'
    },
    {
        'hotel_id': 'charlie',
        'nome': 'Charlie hotel',
        'estrelas': '3.9',
        'diaria': '320.20',
        'cidade': 'Santa Catarina'
    },
]

class Hoteis(Resource):
    def get(self):
        return {'hoteis': [hotel.json() for hotel in HotelModel.query.all()]}

class Hotel(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument('nome', type=str, required=True, help="The field 'nome' cannot be left blank")
    argumentos.add_argument('estrelas', type=float, required=True, help="The field 'estrelas' cannot be left blank")
    argumentos.add_argument('diaria')
    argumentos.add_argument('cidade')    

    def get(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            return hotel.json()
        return {'message': 'Hotel not found'}, 404 # not found

    def post(self, hotel_id):
        if HotelModel.find_hotel(hotel_id):
            return {"message": "Hotel id '{}' already exists.".format(hotel_id)}, 400 #bad request

        dados = Hotel.argumentos.parse_args()
        hotel = HotelModel(hotel_id, **dados)
        try:     
            hotel.save_hotel()
        except:
            return {'message': 'An internal error ocurred to save hotel.'}, 500 # internal server error
        return hotel.json()
        

    def put(self, hotel_id):
        dados = Hotel.argumentos.parse_args()            
        hotel_encontrado = HotelModel.find_hotel(hotel_id)
        if hotel_encontrado:
            hotel_encontrado.update_hotel(**dados)
            hotel_encontrado.save_hotel()
            return hotel_encontrado.json(), 200
        hotel = HotelModel(hotel_id, **dados)
        try:     
            hotel.save_hotel()
        except:
            return {'message': 'An internal error ocurred to save hotel.'}, 500 # internal server error
        return hotel.json(), 201 # created

    def delete(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            try:
                hotel.delete_hotel()
            except:
                return {'message': 'An internal error ocurred to delete hotel.'}, 500 # internal server error
            return {'message': 'Hotel deleted.'}
        return {'Message': 'Hotel not found.'}, 404