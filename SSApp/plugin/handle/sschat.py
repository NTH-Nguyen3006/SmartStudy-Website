import requests
from django.conf import settings

GENAI_KEYS: list = settings.GENAI_KEYS
print(GENAI_KEYS)

def generateResponse(user_message, RETRIES=len(GENAI_KEYS)) -> dict | None:
    localData = open(file="./local_data.txt", mode="r", encoding="utf8").read()
    prompt = f'''
{localData}
    
Kết hợp dữ liệu cho trước như trên hãy trả lời câu hỏi sau theo kiểu tương tác tự nhiên nhất, nếu câu hỏi không khớp với dữ liệu cho trước bạn có thể tự trả lời theo những kiến thức mà bạn đã được biết, một cách chi tiết nhất: 

{user_message}
'''
    url = f'https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={GENAI_KEYS[RETRIES-1]}'
    header = {"Content-Type": "application/json"}
    body = {
        "contents": [
            {
                'role': "user",
                'parts': [{ 'text': localData + prompt + user_message }],
            },
        ]
    }
    
    try:
        # code to try
        response = requests.post(url=url, headers=header, json=body)
        data = response.json()
    except:
        data = generateResponse(user_message=user_message, RETRIES=RETRIES-1)
        print("token GenAI...")
        if RETRIES == 0:
            data = None
        
    return data
        

