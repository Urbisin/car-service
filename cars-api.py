from uuid import uuid4

from flask import Flask, jsonify, request
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient('mongodb://localhost:27017')
db = client['cars_db']
cars_collection = db['cars']

@app.route('/cars', methods=['GET'])
def get_cars():
    cars = list(cars_collection.find({}, {'_id': 0 }))
    return jsonify(cars)

@app.route('/cars/<car_id>', methods=['GET'])
def get_car_id(car_id):
    car = cars_collection.find_one({'_id': car_id})
    if car is None:
        return jsonify({"message": 'Car not found'}), 404
    return jsonify(car)

@app.route('/cars', methods=['POST'])
def add_car():
    cars = request.json
    for car in cars:
        if 'brand' not in car or 'model' not in car or 'year' not in car or 'image_url' not in car or 'type' not in car or 'description' not in car:
            return jsonify({"message": 'Missing required fields'}), 400
       
        brand = car['brand']
        model = car['model']
        type = car['type']
        year = car['year']
        image_url = car['image_url']
        description = car['description']
        status = 'available'

        new_car = {
            '_id': str(uuid4()),
            'brand': brand,
            'model': model,
            'type': type,
            'year': year,
            'image_url': image_url,
            'description': description,
            'status': status
        }
        cars_collection.insert_one(new_car)

    return jsonify({"message": 'Car added successfully'}), 200

@app.route('/cars/<car_id>', methods=['PUT'])
def update_car(car_id):
    car_data = request.json
    car = cars_collection.find_one({'_id': car_id})
    if car is None:
        return jsonify({"message": 'Car not found'}), 404
        
    updated_car = {
        'brand': car_data['brand'],
        'model': car_data['model'],
        'type': car_data['type'],
        'year': car_data['year'],
        'image_url': car_data['image_url'],
        'description': car_data['description'],
        'status': car_data['status']
    }
    cars_collection.update_one({'_id': car_id}, {'$set': updated_car})
    return jsonify({"message": 'Car updated successfully'}), 200

if __name__ == '__main__':
    app.run(debug=True)