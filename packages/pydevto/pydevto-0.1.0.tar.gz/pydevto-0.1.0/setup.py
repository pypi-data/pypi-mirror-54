# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['pydevto']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.8,<5.0', 'requests>=2.22,<3.0']

setup_kwargs = {
    'name': 'pydevto',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': "'Loftie",
    'author_email': 'lpellis@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
