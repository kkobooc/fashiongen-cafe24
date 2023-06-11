# CAFE 24 -> GPT Fine Tuning
## 모듈 구조 설명
### CAFE 24 부분
- start_auth.py
    - CAFE24 쇼핑몰 ID, 인증 코드로 최초 토큰 발급
- get_auth.py
    - CAFE24 access token 유효성을 검증하고, 토큰 만료시 refresh token을 활용하여 토큰 재발급
- db_crud.py
    - db/ 폴더에 json 형식으로 쇼핑몰별 CAFE24 토큰을 DB에 저장하여 읽거나 씀
    - 현재 임시 DB 역할로 json파일 형식을 쓰고 있지만 추후 DB 구축 필요
- get_text.py
    - CAFE24 API를 활용하여 상품 목록과 상품 설명 텍스트를 불러오고, text/ 디렉토리에 저장
### OPEN AI 부분
- train.py
    - Open AI 파인튜닝 형태로 데이터를 변환
    - 모델 학습 및 추론
### 실행 파일
- main.py
    - 위 모듈들을 순차적으로 실행하는 메인 파일
## 파일 및 디렉토리 설명
- .env
    - CAFE24 Client/Secret Key, CAFE24 API 버전, Open AI API Key 등의 환경 변수를 저장
    - gitignore로 숨김 처리
- db/
    - 쇼핑몰별 토큰 데이터
- text/
    - 쇼핑몰별 전처리 전/후 상품 설명 텍스트 데이터
- data/
    - /text/의 데이터 기반 Fine Tuning이 가능한 형태의 데이터가 저장
