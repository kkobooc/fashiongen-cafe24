import json
import openai
import datetime
import time
import pandas as pd
import signal

def get_keyword(mallid, df, api_key):
    openai.api_key = api_key
    keyword_lst = []
    for i, text in enumerate(df["refined_description"]):
        idx = i+1
        # print(prompt)
        while True:
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        # {"role": "system", "content": "텍스트에서 약 10개에서 15개의 주요 한국어 디자인 키워드를 뽑아 콤마로 나열해줘."},
                        {"role": "system", "content": "텍스트에서 약 10개의 주요 한국어 디자인 키워드를 뽑아 콤마로 나열해줘."},
                        {"role": "user", "content": text}
                    ]
                )
                print(idx, response['choices'][0]['message']['content'])
                keyword_lst.append(response['choices'][0]['message']['content'])
                break
            except Exception as e:
                print(idx, ">>>>>>>> Error occurred:", e)
                print(idx, ">>>>>>>> Waiting for 1 minutes before retrying...")
                time.sleep(60)
                
    df['keyword'] = keyword_lst
    now = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
    df.to_csv(f"./text/{mallid}_text_final_{now}.csv", encoding='utf-8-sig')
    return df
    
def prepare_data(mallid, df, api_key):
    openai.api_key = api_key
    # df = pd.read_csv(f'./text/{mallid}_text_final.csv', index_col=0) # 임시 주석
    # df = pd.read_excel(f'./text/{mallid}_text_final.xlsx', index_col=0)
    df = df.iloc[:1000,]
    train_lst = []
    for i, row in df.iterrows():
        product_name = row['product_name']
        simple_description = row['simple_description']
        keyword = row['keyword']
        refined_description = row['refined_description']
        
        # 질문(prompt)
        prompt = f"""상품명은 {product_name}이고, 요약 설명은 '{simple_description}이고, 특징은 {refined_description}'이야."""
        # 답변
        completion = refined_description
        
        train_dic = {"prompt": prompt, "completion": completion}
        train_lst.append(train_dic)
    # 학습 데이터 저장
    with open(f'./data/{mallid}.jsonl', 'w') as f:
        for item in train_lst:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')
    
    # openai.FineTune.prepare
    # subprocess.run(f'openai tools fine_tunes.prepare_data -f "./data/{mallid}_train.jsonl"'.split(), shell=True, capture_output=True, text=True)

def fine_tune(mallid, training_file_id, api_key):
    openai.api_key = api_key
    create_args = {
	"training_file": training_file_id,
	"model": "davinci",
	"n_epochs": 15,
	# "batch_size": 3,
	# "learning_rate_multiplier": 0.3,
    "suffix": f"{mallid}_{datetime.datetime.now().date()}"
    }

    response = openai.FineTune.create(**create_args)
    job_id = response["id"]
    status = response["status"]

    print(f'Fine-tunning model with jobID: {job_id}.')
    print(f"Training Response: {response}")
    print(f"Training Status: {status}")

def check_tune(job_id):
    # 초기 상황 체크
    def signal_handler(sig, frame):
        status = openai.FineTune.retrieve(job_id).status
        print(f"Stream interrupted. Job is still {status}.")
        return
    print(f'Streaming events for the fine-tuning job: {job_id}')
    signal.signal(signal.SIGINT, signal_handler)

    events = openai.FineTune.stream_events(job_id)
    try:
        for event in events:
            print(f'{datetime.datetime.fromtimestamp(event["created_at"])} {event["message"]}')
        
    except Exception:
        print("Stream interrupted (client disconnected).")
    
    # 진행 상황 체크
    status = openai.FineTune.retrieve(id=job_id)["status"]
    if status not in ["succeeded", "failed"]:
        print(f'Job not in terminal status: {status}. Waiting.')
        while status not in ["succeeded", "failed"]:
            time.sleep(60)
            status = openai.FineTune.retrieve(id=job_id)["status"]
            print(f'Status: {status}')
            
    else:
        print(f'Finetune job {job_id} finished with status: {status}')

    print('Checking other finetune jobs in the subscription.')
    result = openai.FineTune.list()
    print(f'Found {len(result.data)} finetune jobs.')
        
    # return openai.FineTune.list()['data'][-1]['fine_tuned_model']
    return None

def get_answer(prompt, model):
    answer = openai.Completion.create(
    model=model,
    prompt=prompt
    )

    print(answer['choices'][0]['text'])
    return answer['choices'][0]['text']