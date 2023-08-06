# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['configclasses']

package_data = \
{'': ['*']}

extras_require = \
{'dotenv': ['python-dotenv[dotenv]>=0.10.3,<0.11.0'],
 'full': ['tomlkit[toml]>=0.5.8,<0.6.0',
          'python-dotenv[dotenv]>=0.10.3,<0.11.0',
          'pyyaml[yaml]>=5.1,<6.0'],
 'toml': ['tomlkit[toml]>=0.5.8,<0.6.0'],
 'yaml': ['pyyaml[yaml]>=5.1,<6.0']}

setup_kwargs = {
    'name': '12factor-configclasses',
    'version': '0.1.3',
    'description': 'Like dataclasses but for config.',
    'long_description': None,
    'author': 'Pablo Cabezas',
    'author_email': 'pabcabsal@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
