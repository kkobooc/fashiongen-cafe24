import requests
import pandas as pd
import time
import json
from bs4 import BeautifulSoup
import re

def get_product_list(mallid, version, access_token):
    # url = f"https://{mallid}.cafe24api.com/api/v2/mains/2/products?limit=100" # 메인상품
    df = pd.DataFrame()
    for i in range(0, 1500, 100):
        print(i)
        url = f"https://{mallid}.cafe24api.com/api/v2/admin/products?limit=100&offset={i}"
        headers = {
            'Authorization': f"Bearer {access_token}",
            'Content-Type': "application/json",
            'X-Cafe24-Api-Version': f"{version}",
            }
        response = requests.request("GET", url, headers=headers)
        print("응답결과 :", response.status_code)
        data = response.json()
        tmp_df = pd.DataFrame(data['products'])
        df = pd.concat([df, tmp_df])
        print(df)
        time.sleep(0.9)
    df = df[(df["display"]=="T") & (df["selling"]=="T")]
    print(f'총 {len(df)}개의 판매 및 진열 상품 불러오기 완료')
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
        lst.append([product_id, response.json()['product']['product_name'],
                    response.json()['product']['simple_description'],
                    response.json()['product']['description']])
        df = pd.DataFrame(lst, columns=["product_id", "product_name", "simple_description", "description"])
        df.to_csv(f"./text/{mallid}_text_raw.csv", encoding='utf-8-sig')
        time.sleep(0.3)
    return df

def preprocess_text(mallid, raw_df):
    # df = pd.read_csv("./text/{mallid}_text_raw.csv")
    
    # HTML 태그 제거
    lst = []
    for text in raw_df["description"]:
        soup = BeautifulSoup(text, 'html.parser')
        html_removed = soup.get_text()
        clean_text = re.sub(r'\n{2,}', '\n', html_removed)
        clean_text = clean_text.strip()
        lst.append(clean_text)
    
    preprocessed_df = raw_df
    preprocessed_df["description"] = lst
    preprocessed_df.to_csv(f"./text/{mallid}_text_preprocessed.csv", encoding='utf-8-sig')
    return preprocessed_df