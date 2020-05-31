from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required
from db import db
from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, Items
from resources.store import Store, StoreList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'makk'
api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()

jwt = JWT(app, authenticate, identity) # /auth

api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(Items, '/items')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(UserRegister, '/register')

if __name__ == "__main__":
    db.init_app(app)
    app.run(port=5000, debug=True)

# in-memory database, won't be necessary
# items = [
#     {
#         "name":"Yeezy Boost",
#         "price": 12.00
#     },
#     {
#         "name":"Yamaha Piano",
#         "price": 15.00
#     }
# ]

#class Student(Resource):
#    def get(self, name):
#        return {'student': name}

# class Items(Resource):
#     def get(self):
#         if len(items) == 0:
#             return {'items':None}, 404
#         else:
#             return {'items':items}

# class Item(Resource):
#     parser = reqparse.RequestParser()
#     parser.add_argument('price',
#         type=float,
#         required=True,
#         help="This field cannot be left blank!"
#         )
    
#     @jwt_required()
#     def get(self, name):
#         #for item in items:
#         #    if item['name'] == name:
#         #        return item
#         item = next(filter(lambda x: x['name'] == name, items),None)
#         return {'item': item}, 200 if item is not None else 404

#     def post(self, name):        
#         if next(filter(lambda x: x['name'] == name, items),None) is not None:
#             return {'message': 'Item with name {} already exists'.format(name)}, 400
    
#         data = Item.parser.parse_args()

#         data = request.get_json()
#         item = {'name':name, 'price': data['price']}
#         items.append(item)
#         return item, 201

#     @jwt_required()
#     def delete(self, name):
#         global items
#         items = list(filter(lambda x: x['name'] != name, items))
#         return {'message': 'Item deleted'}

#     def put(self, name):
#         data = Item.parser.parse_args()

#         item = next(filter(lambda x: x['name'] == name, items),None)
#         if item is None:
#             item = {'name':name, 'price': data['price']}
#             items.append(item)
#         else:
#             item.update(data)
#         return item