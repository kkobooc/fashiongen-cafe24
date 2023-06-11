import json
import openai
import datetime

def prepare_data(mallid):
    with open(f'./text/{mallid}_text_preprocessed.json', 'r') as file:
        text_lst = json.load(file)
        
    train_lst = []
    for text in text_lst:
        # 질문(prompt)
        prompt = f"""다음 의류 상품의 특징을 활용해서 상품 디자인 설명을 써줘."""
        # 답변
        completion = text
        
        train_dic = {"prompt": prompt, "completion": completion}
        train_lst.append(train_dic)
    # 학습 데이터 저장
    with open(f'./data/{mallid}.jsonl', 'w') as f:
        for item in train_lst:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')
    
    openai.FineTune.prepare

def fine_tune(mallid, training_file_id):
    create_args = {
	"training_file": training_file_id,
	"model": "davinci",
	"n_epochs": 15,
	"batch_size": 3,
	"learning_rate_multiplier": 0.3,
    "suffix": f"{mallid}_{datetime.datetime.now().date()}"
    }

    response = openai.FineTune.create(**create_args)
    job_id = response["id"]
    status = response["status"]

    print(f'Fine-tunning model with jobID: {job_id}.')
    print(f"Training Response: {response}")
    print(f"Training Status: {status}")

def get_answer(prompt, model):
    answer = openai.Completion.create(
    model=model,
    prompt=prompt
    )

    print(answer['choices'][0]['text'])
    return answer['choices'][0]['text']