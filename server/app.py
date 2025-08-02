from datetime import datetime

from flask import Flask
from flask import jsonify
from flask import request
from flask_cors import CORS
from pymongo import MongoClient
from bson.objectid import ObjectId
from dataclasses import asdict

from models import User
from models import UserPreferences

import time


app = Flask(__name__)
CORS(app)

client = MongoClient('mongodb://localhost:27017')
db = client['user_crud_db']
collection = db['users']


def serialize_user(user_doc):
    user_doc['_id'] = str(user_doc['_id'])

    if 'preferences' in user_doc and isinstance(user_doc['preferences'], dict):
        pass
    elif 'preferences' in user_doc:
        user_doc['preferences'] = asdict(user_doc['preferences'])

    if 'created_ts' in user_doc and isinstance(user_doc['created_ts'], (int, float)):
        user_doc['created_ts'] = datetime.utcfromtimestamp(user_doc['created_ts']).isoformat() + 'Z'

    if 'updated_ts' in user_doc and isinstance(user_doc['updated_ts'], (int, float)):
        user_doc['updated_ts'] = datetime.utcfromtimestamp(user_doc['updated_ts']).isoformat() + 'Z'

    return user_doc



@app.route('/users', methods=['GET'])
def get_users():
    users = list(collection.find())
    
    serialized_users = []
    for user in users:
        serialized_users.append(serialize_user(user))

    return jsonify(serialized_users), 200


@app.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    user = collection.find_one({'_id': ObjectId(user_id)})

    if user:
        return jsonify(serialize_user(user)), 200
    return jsonify({'error': 'User not found'}), 404


@app.route('/users/username/<username>', methods=['GET'])
def get_user_by_username(username):
    user = collection.find_one({'username': username})

    if user:
        return jsonify(serialize_user(user)), 200
    return jsonify({'error': 'User not found'}), 404


@app.route('/users', methods=['POST'])
def create_user():
    data = request.json

    required_fields = ['username', 'password', 'roles', 'timezone']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing field: {field}'}), 400
        
    if collection.find_one({'username': data['username']}):
        return jsonify({'error': 'Username already exists'}), 400
    
    preferences = UserPreferences(timezone=data['timezone'])
    user = User(
        username=data['username'],
        password=data['password'],
        roles=data['roles'],
        preferences=preferences,
        active=data.get('active', True),
        created_ts=time.time()  # CORREÇÃO: Adicionar created_ts
    )

    result = collection.insert_one(asdict(user))
    created_user = collection.find_one({'_id': result.inserted_id})
    return jsonify(serialize_user(created_user)), 201


@app.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.json

    existing_user = collection.find_one({'_id': ObjectId(user_id)})
    if not existing_user:
        return jsonify({'error': 'User not found'}), 404

    update_data = {}

    if 'username' in data:
        new_username = data['username']
        if new_username != existing_user['username']:
            existing = collection.find_one({'username': new_username, '_id': {'$ne': ObjectId(user_id)}})
            if existing:
                return jsonify({'error': 'Username already exists'}), 400
            update_data['username'] = new_username

    if 'password' in data:
        update_data['password'] = data['password']
    if 'roles' in data:
        update_data['roles'] = data['roles']
    if 'preferences' in data and 'timezone' in data['preferences']:
        update_data['preferences.timezone'] = data['preferences']['timezone']
    if 'active' in data:
        update_data['active'] = data['active']

    update_data['updated_ts'] = time.time()

    collection.update_one({'_id': ObjectId(user_id)}, {'$set': update_data})
    return jsonify({'message': 'User updated'}), 200



@app.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = collection.find_one({'_id': ObjectId(user_id)})
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    collection.delete_one({'_id': ObjectId(user_id)})

    return jsonify({'message': 'User deleted successfully'}), 200


if __name__ == '__main__':
    app.run(debug=True, port=5000)