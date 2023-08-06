# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['datastorm', 'datastorm.exceptions', 'datastorm.limits', 'datastorm.utils']

package_data = \
{'': ['*']}

install_requires = \
['google-cloud-datastore>=1.9,<2.0']

setup_kwargs = {
    'name': 'datastorm',
    'version': '0.0.0a7',
    'description': 'Simple and easy to use ODM for Google Datastore. Documentation: https://datastorm-docs.rtfd.io',
    'long_description': None,
    'author': 'JavierLuna',
    'author_email': 'javierlunamolina@gmail.com',
    'url': 'https://github.com/JavierLuna/datastorm',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
