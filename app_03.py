from flask import Flask, request
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)

items = []

class Item(Resource):

    parser = reqparse.RequestParser()
        parser.add_argument('price', 
            type=float, 
            required=True,
            help='This field cannot be empty!'
            )
    
    def get(self, name):
        item = next(filter(lambda x: x['name'] == name, items), None)
        return {'item': item}, 200 if item else 404     

    def post(self, name):
        if next(filter(lambda x: x['name'] == name, items), None):
            return f'An item with name: \'{name}\' already exists', 400
        
        data = Item.parser.parse_args()
        
        item = {'name': name, 'price': data['price']}
        items.append(item)
        return item, 201

    def delete(self, name):
        global items
        items = list(filter(lambda x: x['name'] != name, items))
        return {'message': 'Item deleted'}

    # def put(self, name):
    #     data = request.get_json()
    #     item = next(filter(lambda x: x['name'] == name, items), None)
    #     if item:
    #         item.update(data)
    #     else:
    #         item = {'name': name, 'price': data['price']}
    #         items.append(item)
    #     return item, 201

    def put(self, name):
        data = Item.parser.parse_args()
        item = next(filter(lambda x: x['name'] == name, items), None)
        if item:
            item.update(data)
        else:
            item = {'name': name, 'price': data['price']}
            items.append(item)
        return item, 201    

class ItemList(Resource):

    def get(self):
        return  {'items': items}
    
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')

app.run(port=5000, debug=True)
