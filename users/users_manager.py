from passlib.context import CryptContext
import json

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

DB_FILE = "users.json"


def load_users():
    try:
        with open(DB_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


def save_users(users):
    with open(DB_FILE, "w") as file:
        json.dump(users, file)
