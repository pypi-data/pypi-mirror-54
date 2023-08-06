# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tiktok_bot',
 'tiktok_bot.api',
 'tiktok_bot.bot',
 'tiktok_bot.client',
 'tiktok_bot.models']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.7.4,<0.8.0',
 'loguru>=0.3.2,<0.4.0',
 'pydantic>=0.32.2,<0.33.0',
 'typing-extensions>=3.7.4,<4.0.0']

setup_kwargs = {
    'name': 'tiktok-bot',
    'version': '0.4.4',
    'description': 'Tik Tok API',
    'long_description': '# tiktok-bot\n\n[![Build Status](https://travis-ci.org/sudoguy/tiktok_bot.svg?branch=master)](https://travis-ci.org/sudoguy/tiktok_bot)\n[![Downloads](https://pepy.tech/badge/tiktok-bot)](https://pepy.tech/project/tiktok-bot)\n',
    'author': 'Evgeny Kemerov',
    'author_email': 'eskemerov@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
