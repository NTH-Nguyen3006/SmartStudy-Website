import requests, json, base64, hashlib, datetime, asyncio

from django.conf import settings
from django.contrib.auth.models import User

from .api_base import GenAI, Github
from ..models import History_ChatBot

GENAI_KEYS: list = settings.GENAI_KEYS

def generateResponse(user_message, RETRIES=len(GENAI_KEYS)) -> dict | None:
    localData = open(file=r"SSApp\plugin\exchange\local_data.txt", mode="r", encoding="utf8").read()
    prompt = f'''
Kết hợp dữ liệu cho trước như trên hãy trả lời câu hỏi sau theo kiểu tương tác tự nhiên nhất, nếu câu hỏi không khớp với dữ liệu cho trước bạn có thể tự trả lời theo những kiến thức mà bạn đã được biết, một cách chi tiết nhất: 
'''
    url = f'https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={GENAI_KEYS[RETRIES-1]}'
    header = {"Content-Type": "application/json"}
    data = {
        "contents": [
            {
                'role': "user",
                'parts': [
                    { 'text': localData},
                    { 'text': prompt },
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

def send_message(userMessage: str, **kwargs) -> str:
    retries = len(GENAI_KEYS)
    kwargs = kwargs["kwargs"]
    while(retries != 0): # token lỗi 
        try:
            genai = GenAI(key=GENAI_KEYS[retries-1])
            if kwargs.get('model_bot'):
                model_bot = kwargs.get('model_bot')
                genai.set_training_data_file(folderpath=f"SSApp/plugin/bot-training/{model_bot}")
                
            contents = {
                'role': 'user',
                'parts': [{'text': userMessage}]
            }

            if kwargs.get("base64_file", None): # user send file/image + question/message
                mimeType = kwargs.get("mimeType", None) # application/pdf, Image/png
                base64_file = kwargs.get("base64_file", None)
                contents['parts'].append(
                    { "inline_data": { "mime_type": mimeType, "data": base64_file } }
                )
            
            # contents = history.extend(contents)
            response = genai.send_message_to_GenAI(contents=[contents])
            
            if response:
                model_reply: dict = response['candidates'][0]['content']["parts"]
                content = ""
                for text in model_reply:
                    content += text["text"] + "\n"

                return content
            return '''Vui lòng liên hệ người bảo trì hệ thống thông qua Facebook: 
            -   <a href="https://www.facebook.com/h.nguyen.3006"><b>Hoàng Nguyên</b></a>
            -   <a href="https://www.facebook.com/profile.php?id=61554015584438"><b>Minh Tuấn</b></a>'''

        except Exception as e:
            print(e)
            retries -= 1
            if retries == 0:
                return "request error"
        # send_message(username, userMessage, base64_file, retries)


def get_history_message(username, chatId) -> list[dict]:
    userObj = User.objects.get(username=username)
    historyObj = History_ChatBot.objects.get(userId=userObj.pk)
    url = "URL history message"
    history = requests.get(url=url).json()

    return history
    

def save_contentsGenAI_to_database(username, history: list[dict]):
    try:
        user = User.objects.get(username=username)
        history_messages = History_ChatBot.objects.get(userId=user.pk)
        if history_messages: #người dùng còn trong box tin nhắn
            chatId = history_messages.chat_id

        else: # người dùng tạo box tin nhắn mới
            chatId = hashlib.md5(
                string=f'{datetime.datetime.today().date}'.encode()).hexdigest()
            history_messages = History_ChatBot(
                chat_id=chatId, userId=user.pk,
                filename=f'{username}-{datetime.datetime.today().strftime("%d-%m-%Y")}',)
            history_messages.save()

        json_history_base64 = base64.b64encode(
            json.dumps(history).encode()).decode()
        task_git = Github().create_or_update_file_Async(
            file_base64=json_history_base64,
            path=f"Chat/{user}/{chatId}.json", repository="messages"
        )

    except:
        print("Save history-message is unsuccessful")
        pass