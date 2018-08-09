from django.conf import settings

import base64
import hashlib
from cryptography.fernet import Fernet


class AuthMiddleware(object):

    def process_request(self, request):

        auth_cookie = request.COOKIES.get('auth_token')
        if not auth_cookie:
            return None

        key = hashlib.md5(settings.SECRET_KEY.encode('utf-8')).hexdigest()
        key_64 = base64.urlsafe_b64encode(key.encode('utf-8'))
        cipher_suite = Fernet(key_64)
        raw_token = cipher_suite.decrypt(auth_cookie.encode('utf-8')).decode('utf-8')

        token_parts = raw_token.split('|')
        if len(token_parts) != 4:
            return None
        auth_token_secret_key = token_parts[0]
        user_email = token_parts[1]
        user_name = token_parts[2]
        user_id = token_parts[3]

        if auth_token_secret_key != settings.AUTH_TOKEN_SECRET_KEY:
            return None

        request.auth = {
            'id': user_id,
            'name': user_name,
            'email': user_email
        }

        return None
