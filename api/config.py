import math
from random import random
from datetime import datetime


class Config:

    __languages = {
        'en': {
            'lang': 'e',
            'accept': 'en-gb',
            'iso': 'en'
        },
        'cy': {
            'lang': 'c',
            'accept': 'cy',
            'iso': 'cy'
        }
    }

    __language = 'en'

    cookies = {
        'accepted_cookies_v2': 'true',
    }

    def __init__(self):
        self.advertiserToken = self.__generateAdvertiserId()

    @staticmethod
    def __generateAdvertiserId():
        token = ''
        d = int(datetime.now().timestamp())
        for c in 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx':
            if c != '-':
                r = int((d + random() * 16) % 16)
                d = math.floor(d / 16)
                c = str(hex(r if c == 'x' else (r & 11)))[2:]
            token += c
        return token

    @property
    def base_headers(self):
        return {
            'authority': 'www.s4c.cymru',
            'accept': 'application/json',
            'origin': 'https://www.s4c.cymru',
            'sec-fetch-dest': 'empty',
            'user-agent': (
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) '
                + 'AppleWebKit/537.36 (KHTML, like Gecko) '
                + 'Chrome/80.0.3987.116 Safari/537.36'
            ),
            'content-type': 'application/json',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        }

    @property
    def language(self):
        return self.__languages[self.__language]

    @language.setter
    def set_language(self, lang):
        self.__language = 'en' if lang == 'en' else 'cy'
