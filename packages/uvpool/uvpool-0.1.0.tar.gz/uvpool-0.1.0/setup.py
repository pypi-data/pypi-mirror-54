# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['uvpool']

package_data = \
{'': ['*']}

install_requires = \
['uvloop>=0.13,<0.14']

setup_kwargs = {
    'name': 'uvpool',
    'version': '0.1.0',
    'description': 'A pool of network utilities based on uvloop',
    'long_description': None,
    'author': 'Yehuda Deutsch',
    'author_email': 'yeh@uda.co.il',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
