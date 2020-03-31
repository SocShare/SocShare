from google.oauth2 import id_token
from google.auth.transport import requests

def authenticate(token):
    try:
        # Specify the CLIENT_ID of the app that accesses the backend:
        idinfo = id_token.verify_oauth2_token(token, requests.Request(), '375227693840-d1eeqq1cik0tmcjcg5j0jj9hfd1oe2e0.apps.googleusercontent.com')

        if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise ValueError('Wrong issuer.')
        # ID token is valid. Get the user's Google Account ID from the decoded token.
        return idinfo['sub']
    except ValueError:
        # Invalid token
        return None