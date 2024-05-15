from uuid import uuid4
from pydantic import BaseModel

from fastapi import FastAPI
from pymongo import MongoClient
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title='Car API',
    description='Car API with FastAPI and MongoDB',
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Car(BaseModel):
    brand: str
    model: str
    color: str

    year: int
    type: str
    description: str

    image: str
    stock: int

    price: int
    discount: int
    available: bool


client = MongoClient('mongodb://host.docker.internal:27017')
# client = MongoClient('mongodb://localhost:27017')
db = client['current']['car']


# car crud

@app.post('/car', description="Method to create a new car")
async def create_car(car: Car):
    db.insert_one({
        '_id': str(uuid4()),

        'brand': car.brand,
        'model': car.model,
        'color': car.color,

        'year': car.year,
        'type': car.type,
        'description': car.description,

        'image': car.image,
        'stock': car.stock,

        'price': car.price,
        'discount': car.discount,
        'available': True
    })

    return {'message': 'created'}, 200


@app.get('/car/{_id}', description="Method to read a car by id")
async def read_car(_id: str):
    document = db.find_one({'_id': _id})

    if not document:
        return {'message': 'car not found'}, 404

    return document, 200


@app.put('/car/{_id}', description="Method to update a car by id")
async def update_car(_id: str, car: Car):
    document = db.find_one({'_id': _id})

    if not document:
        return {'message': 'car not found'}, 404

    db.update_one({'_id': _id}, {
        '$set': {
            'brand': car.brand,
            'model': car.model,
            'color': car.color,

            'year': car.year,
            'type': car.type,
            'description': car.description,

            'image': car.image,
            'stock': car.stock,

            'price': car.price,
            'discount': car.discount,
        }
    })

    return {'message': 'updated'}, 200


@app.delete('/car/{_id}', description="Method to delete a car by id")
async def delete_car(_id):
    document = db.find_one({'_id': _id})

    if not document:
        return {'message': 'car not found'}, 404

    db.delete_one({'_id': _id})

    return {'message': 'deleted'}, 200


# car search


@app.get('/car', description="Method to collect all cars")
async def read_car():
    cars = list(db.find())

    if not cars:
        return {'message': 'empty'}, 404

    return cars, 200
