import bcrypt

from django.conf import settings


def encrypt_password(password):
    salt = settings.SECRET_KEY
    encrypted_pass = bcrypt.hashpw(password, salt)
    return encrypted_pass.decode('utf-8')