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
    
    ###### CAFE24
    # # 토큰 리프레시
    # access_token, refresh_token = token_refresh(mallid, refresh_token, client_id, client_secret)
    # # 상품 목록 가져오기
    product_ids = get_product_list(mallid, version, access_token)
    # # 상품 설명 가져오기
    raw_df = get_product_detail(mallid, access_token, version, client_id, product_ids)
    # # 상품 설명 전처리
    preprocessed_df = preprocess_text(mallid, raw_df)
    # # 쇼핑몰별 함수 처리
    if mallid == "fromday":
        custom_preprocessor = "{mallid}_preprocessor"
        refined_df = globals()[custom_preprocessor](preprocessed_df)
    else:
        refined_df = preprocessed_df
    
    ###### OPENAI
    # # 키워드 가져오기
    final_df = get_keyword(refined_df)
    # # 학습 데이터 준비
    # training_file_id = prepare_data(mallid)
    # # 파인튜닝 모델 생성
    # fine_tune(mallid, training_file_id)
    # # 모델 추론 진행
    # get_answer(prompt, model)