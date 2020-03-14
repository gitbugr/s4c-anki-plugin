import re
import json
import requests
from . import config
from datetime import date


class API:

    config = config.Config()

    token = ''
    name = 'Friend'

    def login(self, email, password):
        """
        Logs in and saves session id

        Parameters
        ---
        email : string
            user email
        password : string
            user password
        """
        headers = self.config.base_headers
        headers['Referer'] = 'https://www.s4c.cymru/clic/MyS4C/SignIn'
        data = {
            'proc': 'bws_clic_api.login',
            'jsondata': {
                'token': None,
                'advertising_id': self.config.advertiserToken,
                'current_client_lang_iso_code': self.config.language['iso'],
                'path': 'clic',
                'email': email,
                'password': password
            }
        }
        response = requests.post(
            'https://www.s4c.cymru/capi',
            headers=headers,
            data=json.dumps(data)
        ).json()

        if (response['status'] == 'error'):
            raise ValueError(response['data'])

        self.token = response['token']
        self.get_profile_data()

    def get_profile_data(self):
        headers = self.config.base_headers
        data = {
            'proc': 'bws_clic_api.get_profiles',
            'jsondata': {
                'token': self.token,
                'advertising_id': self.config.advertiserToken,
                'current_client_lang_iso_code': self.config.language['iso'],
                'path': 'clic',
            }
        }
        response = requests.post(
            'https://www.s4c.cymru/capi',
            headers=headers,
            data=json.dumps(data)
        ).json()

        if (response['status'] == 'error'):
            raise ValueError(response['data'])

        self.name = response['data']['profiles'][0]['name']

    def search_programmes(self, query):
        """
        Queries S4C Search for Programmes

        Parameters
        ---
        query : string
            query string
        """
        headers = self.config.base_headers
        headers['Referer'] = 'https://www.s4c.cymru/clic/Categories'
        params = (
            ('lang', self.config.language['lang']),
            ('q', query),
        )

        return requests.get(
            'https://www.s4c.cymru/df/search',
            headers=headers,
            params=params,
        ).json()['progs']

    def full_programme_info(self, pid):
        """
        Gets Full Programme Info

        Parameters
        ---
        pid : int
            Programme id
        """
        headers = self.config.base_headers
        headers['Referer'] = 'https://www.s4c.cymru/clic/programme/' + str(pid)
        params = (
            ('lang', self.config.language['lang']),
            ('programme_id', str(pid)),
            ('show_prog_in_series', 'Y'),
        )

        return requests.get(
            'https://www.s4c.cymru/df/full_prog_details',
            headers=headers,
            params=params,
            cookies=self.config.cookies
        ).json()['full_prog_details'][0]

    def get_subtitle_url(self, filename):
        """
        Gets url for subtitles

        Parameters
        ---
        filename : string
            Subtitles filename
        """
        filename = re.search('(.*)\\..*', filename).group(1)
        return 'https://www.s4c.cymru/sami/' + filename + '.vtt'

    def get_video_url(self, pid):
        """
        Gets Video URL

        Parameters
        ---
        pid : int
            Programme id
        """
        programmeToken = '{}-{}-{}'.format(
            re.search('([a-zA-Z0-9]+-[a-zA-Z0-9]+)-.*', self.token).group(1),
            pid,
            date.today().strftime("%-d/%-m/%Y")
        )

        params = (
            ('feed', 'json'),
            ('programme_id', pid),
            ('signed', '0'),
            ('lang', 'en'),
            ('wowzApplication', 'od'),
            ('extra', 'false'),
            ('mode', 'od'),
            ('appId', 'clic'),
            ('barbStream', 'od'),
            ('barbPlatform', 's4cdotcom'),
            ('applicationType', 'application/x-mpegURL'),
            ('itemName', programmeToken),
            ('tokenId', self.token),
            ('advertisingId', self.config.advertiserToken),
            ('env', 'live'),
            ('adtag', (
                '//www.s4c.cymru/clic/s4cplayer/sponsorship/vast/s4c-' +
                'ident-vast-3.xml'
            )),
            ('resumeTime', '0'),
        )

        response = requests.get(
            'https://www.s4c.cymru/dfv2/player_configuration',
            headers=self.config.base_headers,
            params=params
        ).json()

        return '{}/{}/{}/{}.m3u8'.format(
            response['streamingUrl'],
            response['filename'],
            'hls',
            response['filename']
        )
