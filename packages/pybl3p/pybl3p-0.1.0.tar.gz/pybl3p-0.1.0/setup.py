# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['pybl3p']

package_data = \
{'': ['*']}

install_requires = \
['requests']

setup_kwargs = {
    'name': 'pybl3p',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Gijs Molenaar',
    'author_email': 'gijs@pythonic.nl',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
