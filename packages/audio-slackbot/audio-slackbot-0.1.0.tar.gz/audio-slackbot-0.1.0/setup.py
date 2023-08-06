# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['audio_slackbot']

package_data = \
{'': ['*']}

install_requires = \
['playsound>=1.2,<2.0', 'pyyaml>=5.1,<6.0', 'slackclient==2.2.1']

entry_points = \
{'console_scripts': ['audio_slackbot = audio_slackbot:run']}

setup_kwargs = {
    'name': 'audio-slackbot',
    'version': '0.1.0',
    'description': 'A slack bot which plays sounds from the filesystem upon certain triggers.',
    'long_description': None,
    'author': 'Nikolai Gulatz',
    'author_email': 'nikolai.gulatz@posteo.de',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
