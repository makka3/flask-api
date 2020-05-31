from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

class Items(Resource):
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]}

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help="This field cannot be left blank!"
        )
    parser.add_argument('store_id',
        type=int,
        required=True,
        help="Every item needs a store id"
        )
    # @jwt_required()

    def get(self, name):
        #item = self.get_item_by_name(name)
        item = ItemModel.get_item_by_name(name)
        if item:
            return item.json()
        return {'message': 'item not found'}, 404
    
        #for item in items:
        #    if item['name'] == name:
        #        return item
        # item = next(filter(lambda x: x['name'] == name, items),None)
        # return {'item': item}, 200 if item is not None else 404

    def post(self, name):        
        
        #if self.get_item_by_name(name):
        if ItemModel.get_item_by_name(name):
            return {'message': 'Item with name {} already exists'.format(name)}, 400

        data = Item.parser.parse_args()

        item = ItemModel(name, data['price'], data['store_id'])
        
        try:
            item.save_to_db()
            #self.insert(item)
        except:
            return {"message": "An error occurred inserting the item"}, 500
        
        #items.append(item)
        return item.json(), 201

    @jwt_required()
    def delete(self, name):
        #global items
        #items = list(filter(lambda x: x['name'] != name, items))
        
        #connection = sqlite3.connect('data.db')
        #cursor = connection.cursor()

        #query = "DELETE FROM items WHERE item=?"
        #cursor.execute(query, (name,))

        #connection.commit()
        #connection.close()
        item = ItemModel.get_item_by_name(name)
        if item:
            item.delete_from_db()

        return {'message': 'Item deleted'}

    def put(self, name):
        data = Item.parser.parse_args()

        #item = next(filter(lambda x: x['name'] == name, items),None)
        
        #item = self.get_item_by_name(name)
        item = ItemModel.get_item_by_name(name)
        #updated_item = {'name':name, 'price': data['price']}
        #updated_item = ItemModel(name, data['price'])

        if item is None:
            item = ItemModel(name, data['price'], data['store_id'])
        else:
            item.price = data['price']
            item.store_id = data['store_id']
        
        item.save_to_db()

        return item.json()

        #    try:
        #        updated_item.save_to_db()
                #ItemModel.insert(updated_item)
                #self.insert(updated_item)
        #    except:
        #        return {"message": "An error occurred inserting the item"}, 500
        #else:
        #    try:
        #        updated_item.update()
                #ItemModel.update(updated_item)
                #self.update(updated_item)
        #    except:
        #        return {"message": "An error occurred updating the item"}, 500
        
        # return updated_item.json()