import json
from utils import load_users, save_users

def authenticate(username, password):
    users = load_users()
    for user in users:
        if user['username'] == username and user['password'] == password:
            return user['role']
    return None

def add_user(username, password, role):
    users = load_users()
    if any(user['username'] == username for user in users):
        return False
    users.append({'username': username, 'password': password, 'role': role})
    save_users(users)
    return True

def update_admin_credentials(new_username, new_password):
    users = load_users()
    for user in users:
        if user['role'] == 'admin':
            user['username'] = new_username
            user['password'] = new_password
            save_users(users)
            return True
    return False