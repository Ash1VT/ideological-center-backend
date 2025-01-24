from fastapi_users.authentication import CookieTransport

transport = CookieTransport(cookie_secure=False)
