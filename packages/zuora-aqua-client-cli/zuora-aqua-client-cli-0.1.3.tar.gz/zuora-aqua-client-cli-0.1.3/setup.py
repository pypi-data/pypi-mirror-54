# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['zuora_aqua_client_cli']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.0,<8.0', 'flake8>=3.7,<4.0', 'requests>=2.22,<3.0']

entry_points = \
{'console_scripts': ['zacc = zuora_aqua_client_cli.run_zoql:main']}

setup_kwargs = {
    'name': 'zuora-aqua-client-cli',
    'version': '0.1.3',
    'description': 'Run ZOQL queries through AQuA from the command line',
    'long_description': None,
    'author': 'Janos Molnar',
    'author_email': 'janosmolnar1001@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
