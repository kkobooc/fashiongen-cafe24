import os
import sys
from get_auth import *
from db_crud import *
from get_text import *
from train import *
# from train import *

if __name__ == "__main__":
    print(sys.argv)
    if len(sys.argv) != 2:
        print("Insufficient arguments")
        sys.exit()
        
    mallid = sys.argv[1]
    
    access_token, refresh_token = read_token(mallid)
    
    if access_token == 0:
        print("Get auth code of '{mallid}'")
        sys.exit()    
    
    version, client_id, client_secret, api_key = get_env()
    os.environ["OPENAI_API_KEY"] = api_key
    
    # -- cafe 24
    # 토큰 리프레시
    access_token, refresh_token = token_refresh(mallid, refresh_token, client_id, client_secret)
    # 상품 목록 가져오기
    product_ids = get_product_list(mallid, version, client_id)
    # 상품 설명 가져오기
    get_product_detail(mallid, access_token, version, client_id, product_ids)
    # 상품 설명 전처리
    preprocess_text(mallid)
    
    # -- openai
    # 학습 데이터 준비
    # training_file_id = prepare_data(mallid)
    # 파인튜닝 모델 생성
    # fine_tune(mallid, training_file_id)
    # 모델 추론 진행
    # get_answer(prompt, model)