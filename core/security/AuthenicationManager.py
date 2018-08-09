import hashlib
import base64
from cryptography.fernet import Fernet

from django.conf import settings

from core.security.CookieManager import CookieManager

class AuthenticationManager:

    def __init__(self):
        self.cookieManager = CookieManager()
        self.auth_token_cookie_name = 'auth_token'  # TODO: move to settings

    def hash_password(self, password):
        password_hash = hashlib.md5(password.encode('utf-8')).hexdigest()
        return password_hash

    def authenticate_response(self, response, user):
        key = hashlib.md5(settings.SECRET_KEY.encode('utf-8')).hexdigest()
        key_64 = base64.urlsafe_b64encode(key.encode('utf-8'))
        cipher_suite = Fernet(key_64)

        raw_token = settings.AUTH_TOKEN_SECRET_KEY + '|' + user.email \
                    + '|' + user.name + '|' + str(user.id)
        token = cipher_suite.encrypt(raw_token.encode('utf-8'))
        # plain_text = cipher_suite.decrypt(cipher_text)

        # token = hashlib.md5(raw_token.encode('utf-8')).hexdigest()

        # TODO: move out from this class
        self.cookieManager.set_cookie(response, self.auth_token_cookie_name, token, days_expire=7)

        return response