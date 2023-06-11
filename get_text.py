import requests
import pandas as pd
import time
import json
from bs4 import BeautifulSoup
import re

def get_product_list(mallid, version, client_id):
    url = f"https://{mallid}.cafe24api.com/api/v2/mains/2/products?limit=100"
    headers = {
        'Content-Type': "application/json",
        'X-Cafe24-Api-Version': f"{version}",
        'X-Cafe24-Client-Id': f"{client_id}"
        }
    response = requests.request("GET", url, headers=headers)
    print(response.status_code)
    data = response.json()
    df = pd.DataFrame(data['products'])
    print(f'총 {len(df)}개의 메인 상품 불러오기 완료')
    print(df[['product_no', 'product_name']])
    return df['product_no'].to_list()

def get_product_detail(mallid, access_token, version, client_id, product_ids):
    lst = []
    print(f"총 {len(product_ids)}개 상품 설명 불러오기..")
    for product_id in product_ids:
        url = f"https://{mallid}.cafe24api.com/api/v2/admin/products/{product_id}"
        headers = {
            'Authorization': f"Bearer {access_token}",
            'Content-Type': "application/json",
            'X-Cafe24-Api-Version': f"{version}",
            'X-Cafe24-Client-Id': f"{client_id}"
            }
        response = requests.request("GET", url, headers=headers)
        print(product_id, response.status_code)
        lst.append([product_id, response.json()['product']['description']])
        time.sleep(0.3)
    
    with open(f'./text/{mallid}_text_raw.json', 'w') as file:
        json.dump(lst, file, ensure_ascii=False)
    
    return None

def preprocess_text(mallid):
    with open(f'./text/{mallid}_text_raw.json', 'r') as file:
        text_lst = json.load(file)
    
    lst = []
    for text in text_lst:
        real_text = text[1]
        soup = BeautifulSoup(real_text, 'html.parser')
        html_removed = soup.get_text()
        clean_text = re.sub(r'\n{2,}', '\n', html_removed)
        clean_text = clean_text.strip()
        lst.append(clean_text)
    
    with open(f'./text/{mallid}_text_preprocessed.json', 'w') as file:
        json.dump(lst, file, ensure_ascii=False)

    return None