from datetime import datetime, timedelta


class CookieManager:

    def set_cookie(self, response, key, value, days_expire=7):
        if days_expire is None:
            max_age = 365 * 24 * 60 * 60  # one year
        else:
            max_age = days_expire * 24 * 60 * 60
        expires = datetime.strftime(datetime.utcnow() + timedelta(seconds=max_age),
                                    "%a, %d-%b-%Y %H:%M:%S GMT")
        response.set_cookie(key, value, max_age=max_age, expires=expires)

    def delete_cookie(self, response, key):
        response.delete_cookie(key)