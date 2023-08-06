# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['uvpool',
 'uvpool.web',
 'uvpool.web.handlers',
 'uvpool.web.logging',
 'uvpool.web.middleware',
 'uvpool.web.views']

package_data = \
{'': ['*']}

install_requires = \
['sanic>=19.9.0,<20.0.0']

extras_require = \
{'rollbar': ['rollbar>=0.14.7,<0.15.0'], 'sentry': ['raven>=6.10.0,<7.0.0']}

setup_kwargs = {
    'name': 'uvpool-web',
    'version': '0.1.1',
    'description': 'A sanic based web framework',
    'long_description': '# UVPool Web\n\nA web framework based on Sanic using the uvloop async event loop by default\n\n## Credits\n\nInitial work on this was done while working at [zencity.io](https://zencity.io/)\n',
    'author': 'Yehuda Deutsch',
    'author_email': 'yeh@uda.co.il',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/uda/uvpool',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
