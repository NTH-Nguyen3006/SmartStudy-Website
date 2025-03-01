import requests, datetime, os, asyncio, base64, mimetypes
import google.generativeai as genai

from django.conf import settings
# from django.contrib.auth.models import User
from concurrent.futures import ThreadPoolExecutor
# from ..models import History_ChatBot

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload


class Github(): 
    # api github docs: https://docs.github.com/en/rest/repos/contents?apiVersion=2022-11-28
    URL_REPOS_API = "https://api.github.com/repos/SmartStudy-ChatBot/{repo}/contents/{path}"
    HEADERS = {
        "Authorization": f"Bearer {settings.GITHUB_KEY}",
        'Accept': 'application/vnd.github+json',
        "X-GitHub-Api-Version": "2022-11-28"
    }
    data = {
        "message": f"{datetime.datetime.now()}",
    }

    def get_repo_content(self, repository, path) -> dict:
        response = requests.get(url=self.URL_REPOS_API.format(
            repo=repository, path=path
        ), headers=self.HEADERS)

        if response.status_code == 200:
            return response.json()
        else:
            raise f'Image not found on repository "{repository}"'

    def create_or_update_file(self, file_base64, path, repository):
        self.data["content"] = file_base64
        response = requests.put(url=self.URL_REPOS_API.format(
            repo=repository, path=path), headers=self.HEADERS, json=self.data)
        return response.json()

    def delete_file(self, path, repository):
        get_image_json = self.get_repo_content(repository=repository, path=path)
        self.data["sha"] = get_image_json["sha"]

        response = requests.delete(url=self.URL_REPOS_API.format(
            repo=repository, path=path), headers=self.HEADERS, json=self.data)
        return response.json()


class Google():
    # google drive docs: https://developers.google.com/drive/api/quickstart/python?hl=vi
    SCOPES = ['https://www.googleapis.com/auth/drive']
    SERVICE_ACCOUNT_FILE = r"SSApp\plugin\exchange\smart-study-441902-37e37affcd03.json"
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build("drive", "v3", credentials=credentials)
    
    def upload(self, filename, mimeType='application/pdf') -> dict | None:
        try:
            # create drive api client
            file_metadata = {"name": filename}
            media = MediaFileUpload(filename, mimetype=mimeType)
            file = self.service.files().create(
                body=file_metadata, media_body=media, fields="name, id").execute()
            
            self.service.permissions().create(
                fileId=file['id'],
                body={'type': 'anyone', 'role': 'reader'},
                fields='id'
            ).execute()

        except HttpError as error:
            print(f"An error occurred: {error}")
            file = None
        return file

    def get_all_files(self, mimeType='application/pdf') -> list[dict]:
        try:
            # create drive api client
            files = []
            page_token = None
            while True:
                response = self.service.files().list(
                        q=f"mimeType='{mimeType}'",
                        spaces="drive",
                        fields="nextPageToken, files(id, name)",
                        pageToken=page_token,
                    ).execute()
                
                # for file in response.get("files", []):
                #     print(f'Found file: {file.get("name")}, {file.get("id")}')
                files.extend(response.get("files", []))
                page_token = response.get("nextPageToken", None)
                if page_token is None:
                    return files
        except HttpError as error:
            print(f"An error occurred: {error}")
            files = None

    def delete_file(self, fileId) -> None:
        try:
            # create drive api client
            self.service.files().delete(fileId=fileId).execute()

        except HttpError as error:
            print(f"An error occurred: {error}")
            files = None

        print(f'deleted file id -> "{fileId}"')


class GenAI:
    def __init__(self, key:str, model="gemini-2.0-flash"):
        self.model = model
        self.URL_GENAI = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent?key={key}"
        self.HEADERS = {"Content-Type": "application/json"}
        self.TRAINING = [
            {
                "role": "user",
                "parts": [
                    {"text": open(file=r"SSApp\plugin\exchange\local_data.txt", mode="r", encoding="utf8").read()},
                    {"text": "Kết hợp dữ liệu cho trước như trên hãy trả lời câu hỏi sau theo kiểu tương tác tự nhiên nhất, nếu câu hỏi không khớp với dữ liệu cho trước bạn có thể tự trả lời theo những kiến thức mà bạn đã được biết, một cách chi tiết nhất."}
                ]
            },
            {
                'role': 'model',
                'parts': [
                    {"text":"Okay, sẵn sàng trả lời câu hỏi rồi đây! Hãy cứ hỏi đi nhé."}
                ]
            }
        ]
        
    def send_message_to_GenAI(self, contents:list[dict]) -> dict | None:
        try:
            if contents:
                self.TRAINING.extend(contents)
                data = {"contents": self.TRAINING}
                response = requests.post(
                    url=self.URL_GENAI, headers=self.HEADERS, json=data)
                if response.status_code == 200:
                    response_json = response.json()
                    model_contents = response_json["candidates"][0]["content"]
                    self.TRAINING.append(model_contents)
                    return response_json
                else: 
                    return None
            return "Generate contents error"
        
        except Exception as e:
            raise e
    
    def send_question_file_GenAI(self, contents) -> str:
        try:
            if contents:
                data = {"contents": contents}
                response = requests.post(
                    url=self.URL_GENAI, headers=self.HEADERS, json=data)
                
                if response.status_code == 200:
                    return response.json()
                else: 
                    return "Bad request"
            return "Generate contents error"
        
        except Exception as e:
            raise e
        
    def set_training_data_text(self, data_text: str = None, file_train=None) -> None:
        if file_train:
            data_text = open(
                file=file_train, mode="r", encoding="utf8").read()
            
        data: dict = {
            "role": "user",
            "parts": [
                {"text": data_text},
                {"text": "Kết hợp dữ liệu cho trước như trên hãy trả lời câu hỏi sau theo kiểu tương tác tự nhiên nhất, nếu câu hỏi không khớp với dữ liệu cho trước bạn có thể tự trả lời theo những kiến thức mà bạn đã được biết, một cách chi tiết nhất."}
            ]
        }
        self.TRAINING.append(data)

    def set_training_data_file(self, folderpath: str, prompt=None):
        inline_datas = []
        for path in os.listdir(folderpath):
            with open(f'{folderpath}/{path}', mode="rb") as readfile:
                base64_file = base64.b64encode(readfile.read()).decode()
                mimeType, encoding = mimetypes.guess_type(path)
                inline_datas.append({
                    "inline_data": {"mime_type": mimeType, "data": base64_file}
                })

        subjects = {
            "geography": "địa lý", 'history': 'lịch sử', 
            "legal-economics": 'kinh tế pháp luật'
        }
        data = {
            'role': 'user',
            'parts': inline_datas + [
                {'text': f"Bạn là giáo viên môn {subjects.get(os.path.basename(folderpath))}, bạn hãy học toàn bộ nội dung từ file trên và trả lời các câu hỏi sau tự nhiên nhất và chi tiết nhất. Nếu trường hợp câu hỏi không nằm tron dữ liệu cho trước thì bạn hãy dùng dữ liệu mà bạn được biết hoặc được cung cấp để trả lời một cách tự nhiên nhất"},
            ]
        }
        self.model = "gemini-2.0-flash-exp"
        # self.TRAINING = [data]
        self.TRAINING.append(data)
    

    

        
        

