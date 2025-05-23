import json
import os

import requests
from app.extensions import logging


class Model(object):
    def __init__(self, api_key=None):
        self.api_key = api_key

    def query(self, message=None, model=None):
        raise NotImplementedError(
            'Subclasses must implement the query method.')


class OpenRouter(Model):
    """
    Models: https://openrouter.ai/models?order=pricing-low-to-high
    Kwargs: https://openrouter.ai/docs/api-reference/parameters
    """

    def __init__(self, api_key=None, api_url='https://openrouter.ai/api/v1', query_path='/chat/completions'):
        if api_key is None:
            api_key = os.environ[f'API_{self.__class__.__name__.upper()}_KEY']

        super().__init__(api_key=api_key)

        self.api_url = api_url
        self.query_path = query_path

    def query(self, message, model='sophosympatheia/rogue-rose-103b-v0.2:free'):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + self.api_key,
        }

        payload = {
            'model': model,
            'messages': [
                {
                    'role': 'user',
                    'content': message,
                },
            ],
        }

        response = requests.post(
            f'{self.api_url}{self.query_path}', headers=headers, json=payload)

        if response.status_code != 200:
            logging.error(
            f'[LLM (OpenRouter)] Error in response: {response.content}')
            return None

        content = response.content.strip()
        try:
            data = json.loads(content)
            for i in data.get('choices', []):
                return i.get('message', {}).get('content', None).strip()
        except:
            return None


class LLM(object):
    Providers = {
        'OpenRouter': OpenRouter
    }

    def __init__(self, api_key=None):
        self.api_key = api_key

    def query(self, message=None, provider='OpenRouter'):
        p = LLM.Providers[provider](api_key=self.api_key)
        return p.query(message=message)
