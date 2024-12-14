import requests, json

with open("config.json", "r") as read_json:
    data: dict = json.load(read_json)
GENAI_KEYS: list = data.get("GenAI-Key")

def generateResponse(user_message, RETRIES=len(GENAI_KEYS)) -> dict | None:
    training_data = open(r'training-bot\trainingdata.txt', mode='r', encoding='utf8').read()
    url = f'https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={GENAI_KEYS[RETRIES-1]}'
    header = {"Content-Type": "application/json"}
    data = {
        "contents": [
            {
                'role': "user",
                'parts': [
                    {"text": training_data},
                    {'text': "Kết hợp dữ liệu cho trước như trên hãy trả lời câu hỏi sau theo kiểu tương tác tự nhiên nhất, nếu câu hỏi không khớp với dữ liệu cho trước bạn có thể tự trả lời theo những kiến thức mà bạn đã được biết, một cách chi tiết nhất."},
                ],
            },
            {
                'role': "user",
                'parts': [
                    { 'text': user_message },
                ],
            },
        ]
    }
    
    try:
        response = requests.post(url=url, headers=header, json=data)
        data = response.json()
    except:
        print("token GenAI...")
        data = generateResponse(user_message=user_message, RETRIES=RETRIES-1)
        if RETRIES == 0:
            data = None
        
    return data

