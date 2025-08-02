import json
from datetime import datetime
from pymongo import MongoClient
from dataclasses import asdict

from models import User
from models import UserPreferences


def parse_roles(user_data):
    roles = []

    if user_data.get('is_user_admin', False):
        roles.append('admin')
    if user_data.get('is_user_manager', False):
        roles.append('manager')
    if user_data.get('is_user_tester', False):
        roles.append('tester')

    return roles

def parse_created_timestamp(created_at_str):
    dt = datetime.fromisoformat(created_at_str.replace('Z', '+00:00'))
    return dt.timestamp()

def main():
    client = MongoClient('mongodb://localhost:27017')
    db = client['user_crud_db']
    collection = db['users']

    with open('../udata.json', 'r') as file:
        data = json.load(file)

    users_to_insert = []
    for user_data in data['users']:
        roles = parse_roles(user_data)
        preferences = UserPreferences(timezone=user_data['user_timezone'])
        created_ts = parse_created_timestamp(user_data['created_at'])

        user = User(
            username=user_data['user'],
            password=user_data['password'],
            roles=roles,
            preferences=preferences,
            active=user_data['is_user_active'],
            created_ts=created_ts,
            updated_ts=created_ts
        )

        users_to_insert.append(asdict(user))

    result = collection.insert_many(users_to_insert)
    print(f"Successfully imported {len(result.inserted_ids)} users to MongoDB")

if __name__ == "__main__":
    main()