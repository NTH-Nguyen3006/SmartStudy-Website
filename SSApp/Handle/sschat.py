import requests, os
from dotenv import load_dotenv
load_dotenv(r"C:\Users\Admin\Desktop\SS_Website\.env.example", encoding="utf8")

# GENAI_KEYS: list = eval(os.environ["GENAI_KEYS"])

def generateResponse(user_message, RETRIES=3) -> dict | None:
    localData = open(file="SSApp\Handle\local_data.txt", mode="r", encoding="utf8").read()
    print(user_message)
    prompt = f'''
{localData}
    
Kết hợp dữ liệu cho trước như trên hãy trả lời câu hỏi sau theo kiểu tương tác tự nhiên nhất, nếu câu hỏi không khớp với dữ liệu cho trước bạn có thể tự trả lời theo những kiến thức mà bạn đã được biết, một cách chi tiết nhất: 

{user_message}
'''
    # url = f'https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key={GENAI_KEYS[RETRIES-1]}'
    url = f'https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key={"AIzaSyB6VIzIMt-Eax92Zt9GPQeiM0wE2KLo090"}'
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
        if RETRIES == 0:
            data = None
        
    return data
        

