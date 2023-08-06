# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['cfglib', 'cfglib.sources']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'cfglib',
    'version': '0.2.0a3',
    'description': 'An extensible configuration library',
    'long_description': '======\ncfglib\n======\n\n\n.. image:: https://img.shields.io/pypi/v/cfglib.svg\n        :target: https://pypi.python.org/pypi/cfglib\n\n.. image:: https://readthedocs.org/projects/cfglib/badge/?version=latest\n        :target: https://cfglib.readthedocs.io/en/latest/?badge=latest\n        :alt: Documentation Status\n\n\nAn extensible configuration library\n\n\n* Free software: MIT license\n* Documentation: https://cfglib.readthedocs.io.\n\n\nFeatures\n--------\n\n* Describe config schema and perform validation\n* Numerous utils to compose configs from multiple sources, etc.\n* Read settings from environment\n',
    'author': 'Anton Barkovsky',
    'author_email': 'anton@swarmer.me',
    'url': 'https://github.com/swarmer/cfglib-py',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4',
}


setup(**setup_kwargs)
