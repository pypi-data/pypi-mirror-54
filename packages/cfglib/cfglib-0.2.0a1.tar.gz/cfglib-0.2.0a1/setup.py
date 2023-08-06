# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['cfglib', 'cfglib.sources']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'cfglib',
    'version': '0.2.0a1',
    'description': 'An extensible configuration library',
    'long_description': None,
    'author': 'Anton Barkovsky',
    'author_email': 'anton@swarmer.me',
    'url': 'https://github.com/swarmer/cfglib-py',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4',
}


setup(**setup_kwargs)
