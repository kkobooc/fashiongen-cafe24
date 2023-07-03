import re

def fromday_preprocessor(df):
    lst = []
    # 상품 설명 전처리
    for text in df['description']:
        word = r'✔️color*'
        pattern = re.compile(f"{word}.*", re.DOTALL)
        refined_text = re.sub(pattern, "", text)
        lst.append(refined_text)
    df["refined_description"] = lst
    
    # 상품 이름 전처리
    lst = []
    for text in df['product_name']:
        pattern = r"\([^()]*\)"
        refined_text = re.sub(pattern, "", text)
        lst.append(refined_text)
    df["product_name"] = lst
    return df