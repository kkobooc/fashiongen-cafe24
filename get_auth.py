import base64
import requests
from db_crud import *

def get_auth(mallid, auth_code):
    url = f'https://{mallid}.cafe24api.com/api/v2/oauth/token'
    headers = {
        'Authorization': 'Basic SnNkMk4xTnRQRmZOenVwdXA5eDRyQzp3RHg2MEl3TU81UGtyVGpBejRqZlBB',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'grant_type': 'authorization_code',
        'code': auth_code,
        'redirect_uri': 'https://fashiongen.ai/'
    }

    response = requests.post(url, headers=headers, data=data)
    print(response.json())
    access_token, refresh_token = response.json()['access_token'], response.json()['refresh_token']
    write_token(mallid, access_token, refresh_token)
    print(f"---{mallid} AUTH DONE, TOKEN SAVED---")
    return response.json()['access_token'], response.json()['refresh_token']

def token_refresh(mallid, refresh_token, client_id, client_secret):
    client_id_secret = f"{client_id}:{client_secret}"
    encoded_bytes = base64.b64encode(client_id_secret.encode('utf-8'))
    encoded_string = encoded_bytes.decode('utf-8')

    url = f'https://{mallid}.cafe24api.com/api/v2/oauth/token'

    headers = {
        'Authorization': f'Basic {encoded_string}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token
    }
    response = requests.post(url, headers=headers, data=data)
    print(response.json())
    access_token, refresh_token = response.json()['access_token'], response.json()['refresh_token']
    write_token(mallid, access_token, refresh_token)
    return access_token, refresh_token

def check_token_valid(mallid, access_token, refresh_token):
    pass