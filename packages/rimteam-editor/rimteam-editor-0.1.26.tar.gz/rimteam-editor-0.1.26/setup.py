# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['rimteam_editor']

package_data = \
{'': ['*']}

install_requires = \
['gitpython>=3.0,<4.0', 'requests>=2.22,<3.0']

entry_points = \
{'console_scripts': ['reditor = rimteam_editor.__main__:main']}

setup_kwargs = {
    'name': 'rimteam-editor',
    'version': '0.1.26',
    'description': '',
    'long_description': None,
    'author': 'RIM team',
    'author_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
