import requests, datetime

from django.conf import settings

# api github docs: https://docs.github.com/en/rest/repos/contents?apiVersion=2022-11-28
URL_REPOS_API = "https://api.github.com/repos/SmartStudy-ChatBot/{repo}/contents/{path}"
HEADERS = {
    "Authorization": f"Bearer {settings.GITHUB_KEY}",
    'Accept': 'application/vnd.github+json',
    "X-GitHub-Api-Version": "2022-11-28"
}


def get_repo_content(repository, path) -> dict:
    response = requests.get(url=URL_REPOS_API.format(
        repo=repository, path=path
    ), headers=HEADERS)

    if response.status_code == 200:
        return response.json()
    else:
        raise f'Image not found on repository "{repository}"'


def create_or_update_file(image_base64, path, repository):
    data = {
        "content": image_base64,
        "message": f"{datetime.datetime.now()}",
    }

    response = requests.put(url=URL_REPOS_API.format(
        repo=repository, path=path), headers=HEADERS, json=data)
    return response.json()


def delete_file(image_base64, path, repository):
    get_image_json = get_repo_content(repository=repository, path=path)

    data = {
        "content": image_base64,
        "message": "delete file",
        "sha": get_image_json["sha"],
    }

    response = requests.delete(url=URL_REPOS_API.format(
        repo=repository, path=path), headers=HEADERS, json=data)
    return response.json()
