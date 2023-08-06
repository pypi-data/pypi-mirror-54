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
    'version': '0.1.1',
    'description': 'A pool of network utilities based on uvloop',
    'long_description': '# UVPool\n\nA pool of network utilities based on uvloop\n\n## Roadmap\n\n* Web - based on sanic\n* DNS - Full implementation of DNS\n* Mail - Implements SMTP, IMAP and POP3 + support middleware for filtering and rules\n\n### Planned sub-projects\n\n* Web:\n    * WebDAV - CardDAV, CalDAV\n    * RSS feed aggregator\n    * Notes app\n    * Blog\n* DNS:\n    * DDNS (Web interface + DNS Server)\n* Mail:\n    * Webmail - with integration into other apps\n\n',
    'author': 'Yehuda Deutsch',
    'author_email': 'yeh@uda.co.il',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/uda/uvpool.git',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
