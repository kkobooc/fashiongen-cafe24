import json
from dotenv import dotenv_values

def read_token(mallid):
    with open('./db/db.json', 'r') as file:
        data = json.load(file)
    try:
        mall_data = data[mallid]
        return mall_data[0], mall_data[1]
    except Exception as e:
        print(e)
        print('mallid not found in db')
        return [0, 0]

def write_token(mallid, access_token, refresh_token):
    with open('./db/db.json', 'r') as file:
        data = json.load(file)
    
    data[mallid] = [access_token, refresh_token]
    
    with open('./db/db.json', 'w') as file:
        json.dump(data, file)
        
def get_env():
    # Load environment variables from .env file
    env_vars = dotenv_values(".env")

    # Access the environment variables
    version = env_vars.get("VERSION")
    client_id = env_vars.get("CLIENT_ID")
    client_secret = env_vars.get("CLIENT_SECRET")
    api_key = env_vars.get("OPENAI_API_KEY")
    return version, client_id, client_secret, api_key