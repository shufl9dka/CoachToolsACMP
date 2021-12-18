import os
import json
from pathlib import Path

USERS_PATH = os.path.join(Path(__file__).parent.parent, 'users.json')


def load_users() -> list:
    try:
        with open(USERS_PATH, 'r') as f_in:
            return json.load(f_in)
    except Exception:
        return []


def save_users(users: list):
    with open(USERS_PATH, 'w') as f_out:
        json.dump(users, f_out)


def check_user(username: str) -> bool:
    for user in load_users():
        if user['username'].lower() == username:
            return True
    return False


def append_user(new_user: dict):
    users = load_users()
    users.append(new_user)
    save_users(users)
