import requests
from enum import Enum

from settings import MEDIUM_API_TOKEN


class PublishStatusEnum(Enum):
    DRAFT = 'draft'
    PUBLIC = 'public'
    UNLISTED = 'unlisted'


class Medium:
    headers = {
        'Authorization': f'Bearer {MEDIUM_API_TOKEN}',
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Accept-Charset': 'utf-8',
    }

    def __init__(self):
        self.id = self.get_user_info_d().get('id')

        if not self.id:
            raise ValueError('No Medium valid id found.')

    def get_user_info_d(self) -> dict:
        resp = requests.get('https://api.medium.com/v1/me', headers=self.headers)
        resp_d = resp.json()
        return resp_d.get('data', {}) if resp.status_code == 200 else dict()

    def post_article(
            self,
            title: str,
            content: str,
            publish_status: PublishStatusEnum=PublishStatusEnum.DRAFT,
    ) -> dict:
        payload = {
            'title': title,
            'contentFormat': 'html',
            'content': content,
            'publishStatus': publish_status.value
        }

        resp = requests.post(f'https://api.medium.com/v1/users/{self.id}/posts', headers=self.headers, json=payload)
        return resp.json()
