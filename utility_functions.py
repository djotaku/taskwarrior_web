from werkzeug.security import generate_password_hash, check_password_hash
import json


def create_new_password_hash():
    """Create new password has and save to secret_config"""
    username = input("What username do you want?")
    password = input("What should your password be set to?")
    with open("secrets_config", "r") as secrets_file:
        secrets = json.load(secrets_file)
        user = {username: {"password": generate_password_hash(password)}}
        secrets["user"] = user
    with open("secrets_config", "w") as secrets_file:
        json.dump(secrets, secrets_file)
