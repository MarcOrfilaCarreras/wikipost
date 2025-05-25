import asyncio
import email
import imaplib
import json
import random
import re
import threading
from pathlib import Path

import aiohttp
import instagrapi
import requests
from app.extensions import logging
from instagrapi.mixins.challenge import ChallengeChoice
from instagrapi.types import StoryPoll


class EmailCodeRetriever:
    def __init__(self, email_address, password):
        self.email_address = email_address
        self.password = password
        self.mail = None

    def connect(self):
        self.mail = imaplib.IMAP4_SSL('imap.gmail.com')
        self.mail.login(self.email_address, self.password)
        self.mail.select('inbox')

    def fetch_unread_emails(self):
        result, data = self.mail.search(None, '(UNSEEN)')
        if result != 'OK':
            raise Exception(f'Error fetching emails: {result}')
        return data[0].split()

    def extract_code_from_email(self, email_body, username):
        if '<div' not in email_body:
            return None

        code_match = re.search(r'>(\d{6})<', email_body)
        if code_match:
            return code_match.group(1)

        return None

    def get_verification_code(self, username):
        self.connect()
        email_ids = self.fetch_unread_emails()

        for email_id in reversed(email_ids):
            self.mail.store(email_id, '+FLAGS', '\\Seen')
            result, data = self.mail.fetch(email_id, '(RFC822)')
            if result != 'OK':
                raise Exception(f'Error fetching email content: {result}')

            msg = email.message_from_bytes(data[0][1])
            payloads = msg.get_payload() if isinstance(
                msg.get_payload(), list) else [msg]

            for payload in payloads:
                email_body = payload.get_payload(
                    decode=True).decode(errors='ignore')
                code = self.extract_code_from_email(email_body, username)
                if code:
                    return code

        return False


class ProxyManager:
    LOCK = threading.Lock()
    IP = None
    PROXIES = []
    URL = 'https://api.proxyscrape.com/v4/free-proxy-list/get'

    def __init__(self):
        self.thread = threading.Thread(
            target=self.refresh_proxies, daemon=True)
        self.thread.start()

        if ProxyManager.IP is None:
            ProxyManager.IP = self.get_original_ip()

        logging.info(f'[PROXY] Initialized')

    @classmethod
    def get_original_ip(cls):
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:135.0) Gecko/20100101 Firefox/135.0'}
            response = requests.get('https://api.ipify.org', headers=headers)
            return response.text
        except requests.RequestException as e:
            logging.error('[PROXY] Error getting original IP')
            return None

    @classmethod
    async def fetch_proxies(cls):
        logging.info('[PROXY] Fetching new proxies...')

        params = {
            'request': 'display_proxies',
            'country': 'us',
            'proxy_format': 'protocolipport',
            'format': 'json',
            'timeout': '20000'
        }

        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:135.0) Gecko/20100101 Firefox/135.0'}

        try:
            response = requests.get(
                cls.URL, timeout=10, params=params, headers=headers)
            if response.status_code != 200:
                raise requests.exceptions.RequestException(
                    f'Status code was {response.status_code}')

            data = response.json()

            proxies = [
                {'ip': proxy['ip'], 'port': str(
                    proxy['port']), 'protocol': proxy['protocol']}
                for proxy in data['proxies']
                if (proxy.get('uptime', 121) <= 120) and (proxy['protocol'] in ['socks4', 'socks5'])
            ]

            return proxies
        except requests.exceptions.RequestException as e:
            logging.error('[PROXY] Error fetching proxies')
            return []

    @classmethod
    async def test_proxy(cls, proxy, session):
        return True

    @classmethod
    async def refresh_proxies_async(cls):
        async with aiohttp.ClientSession() as session:
            while True:
                logging.info('[PROXY] Starting proxy refresh cycle...')

                new_proxies = await cls.fetch_proxies()
                valid_proxies = []
                tasks = []

                for proxy in new_proxies:
                    tasks.append(cls.test_proxy(proxy, session))

                results = await asyncio.gather(*tasks)
                for proxy, is_valid in zip(new_proxies, results):
                    if is_valid:
                        valid_proxies.append(proxy)

                with cls.LOCK:
                    cls.PROXIES.clear()
                    cls.PROXIES.extend(valid_proxies)

                logging.info(
                    f'[PROXY] Updated proxy list with {len(cls.PROXIES)} valid proxies.')
                await asyncio.sleep(60)

    @classmethod
    def refresh_proxies(cls):
        logging.info('[PROXY] Starting proxy refresh in a separate thread...')
        asyncio.run(cls.refresh_proxies_async())

    @classmethod
    def get_proxy(cls):
        with cls.LOCK:
            if cls.PROXIES:
                proxy = random.choice(cls.PROXIES)
                return proxy

            logging.error('[PROXY] No valid proxies available.')
            return None


class Instagram:
    def __init__(self, username=None, password=None, email_address=None, email_password=None):
        self.username = username
        self.password = password
        self.client = instagrapi.Client()
        self.client.challenge_code_handler = self.challenge_code_handler
        self.email_retriever = EmailCodeRetriever(
            email_address, email_password) if email_address and email_password else None

        proxy = ProxyManager.get_proxy()
        self.client.delay_range = [1, 3]
        self.client.public.proxies = self.client.private.proxies = {
            f"{proxy['protocol']}": f"{proxy['ip']}:{proxy['port']}"}

    def login(self):
        if self.username is None:
            raise ValueError('You must provide the username')
        if self.password is None:
            raise ValueError('You must provide the password')
        self.client.login(username=self.username, password=self.password)

    def upload_photo(self, path=None, description=None):
        if path is None:
            raise ValueError('You must provide the path to the photo')
        if description is None:
            raise ValueError('You must provide the description for the photo')
        return self.client.photo_upload(Path(path), description).pk

    def upload_history(self, path=None, poll=None):
        kwargs = {}

        if path is None:
            raise ValueError('You must provide the path to the photo')

        if poll is not None:
            kwargs['polls'] = [StoryPoll(x = 0.5, y = 0.7, width = 0.7, height = 0.3, question = poll['title'], options = poll['options'])]

        return self.client.photo_upload_to_story(path, **kwargs).pk

    def challenge_code_handler(self, username, choice):
        if choice == ChallengeChoice.EMAIL and self.email_retriever:
            return self.email_retriever.get_verification_code(username)
        return False
