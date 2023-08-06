# -*- coding: utf-8 -*-
from distutils.core import setup

package_dir = \
{'': 'src'}

packages = \
['slackers']

package_data = \
{'': ['*']}

install_requires = \
['fastapi>=0.42,<0.43',
 'pyee>=6.0,<7.0',
 'python-multipart>=0.0.5,<0.0.6',
 'requests>=2.22,<3.0']

setup_kwargs = {
    'name': 'slackers',
    'version': '0.1.0',
    'description': 'Slack interaction webhooks served by FastAPI',
    'long_description': None,
    'author': 'Niels van Huijstee',
    'author_email': 'niels@huijs.net',
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
