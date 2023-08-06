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
    'version': '0.1.6',
    'description': 'Run ZOQL queries through AQuA from the command line',
    'long_description': '# zuora-aqua-client-cli [![Build Status](https://travis-ci.com/molnarjani/zuora-aqua-client-cli.svg?branch=master)](https://travis-ci.com/molnarjani/zuora-aqua-client-cli)\n\nRun ZOQL queries through AQuA from the command line\n\n# Usage\n\n```\n$ zacc --help\n\nUsage: zacc [OPTIONS]\n\nOptions:\n  -c, --config-filename PATH      Config file containing Zuora ouath\n                                  credentials  [default: zuora_oauth.ini]\n  -z, --zoql PATH                 ZOQL file to be executed  [default:\n                                  input.zoql]\n  -e, --environment [prod|preprod|local]\n                                  Zuora environment to execute on  [default:\n                                  local]\n  --help                          Show this message and exit.\n```\n',
    'author': 'Janos Molnar',
    'author_email': 'janosmolnar1001@gmail.com',
    'url': 'https://github.com/molnarjani/zuora-aqua-client-cli',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
