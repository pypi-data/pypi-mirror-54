# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['scdlbot']

package_data = \
{'': ['*'], 'scdlbot': ['texts/*']}

install_requires = \
['Celery==4.3.0',
 'bandcamp-downloader==0.0.8.post12',
 'boltons==19.3.0',
 'logentries==0.17',
 'mutagen==1.42.0',
 'patool==1.12',
 'plumbum==1.6.7',
 'pydub==0.23.1',
 'pyshorteners==0.6.1',
 'python-telegram-bot==10.1.0',
 'python-telegram-handler==2.2',
 'scdl==1.6.12',
 'youtube-dl==2019.10.29']

setup_kwargs = {
    'name': 'scdlbot',
    'version': '0.9.21',
    'description': 'Telegram Bot for downloading MP3 rips of tracks/sets from SoundCloud, Bandcamp, YouTube with tags and artwork',
    'long_description': None,
    'author': 'George Pchelkin',
    'author_email': 'george@pchelk.in',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
