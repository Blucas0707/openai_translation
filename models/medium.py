from typing import List
from enum import Enum

import requests

from settings import MEDIUM_API_TOKEN


class PublishStatusEnum(Enum):
    DRAFT = 'draft'
    PUBLIC = 'public'
    UNLISTED = 'unlisted'


class LicenseEnum(Enum):
    ALL_RIGHTS_RESERVED = 'all-rights-reserved'
    CC_40_BY = 'cc-40-by'
    CC_40_BY_SA = 'cc-40-by-sa'
    CC_40_BY_ND = 'cc-40-by-nd'
    CC_40_BY_NC = 'cc-40-by-nc'
    CC_40_BY_NC_ND = 'cc-40-by-nc-nd'
    CC_40_BY_NC_SA = 'cc-40-by-nc-sa'
    CC_40_ZERO = 'cc-40-zero'
    PUBLIC_DOMAIN = 'public-domain'


class ContentFormatEnum(Enum):
    HTML = 'html'
    MARKDOWN = 'markdown'


class Medium:
    api_url = 'https://api.medium.com/v1'
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
        resp = requests.get(f'{self.api_url}/me', headers=self.headers)
        resp_d = resp.json()
        return resp_d.get('data', {}) if resp.status_code == 200 else {}

    def post_article(
        self,
        title: str,
        content: str,
        tags: List[str] = [],
        to_notify_followers: bool = False,
        contentFormat: ContentFormatEnum = ContentFormatEnum.HTML.value,
        license: LicenseEnum = LicenseEnum.ALL_RIGHTS_RESERVED.value,
        publish_status: PublishStatusEnum = PublishStatusEnum.DRAFT.value,
    ) -> dict:
        payload = {
            'title': title,
            'contentFormat': contentFormat,
            'content': content,
            'tags': tags,
            'license': license,
            'notifyFollowers': to_notify_followers,
            'publishStatus': publish_status,
        }

        resp = requests.post(
            f'{self.api_url}/users/{self.id}/posts',
            headers=self.headers,
            json=payload,
        )
        return resp.json()


def post_article_from_file(filename: str, tags: List[str]):
    from models.article import read_article

    title = filename.replace('.input', '').replace('.output', '')
    article = read_article(filename)
    formatted_article = article.replace('\n', '<br>')

    Medium().post_article(
        title,
        content=formatted_article,
        tags=tags,
    )
