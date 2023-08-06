# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['autoscreenshot']

package_data = \
{'': ['*']}

install_requires = \
['pillow>=6.2.1,<7.0.0',
 'pyperclip>=1.7.0,<2.0.0',
 'pyscreenshot>=0.5.1,<0.6.0',
 'requests>=2.22.0,<3.0.0']

setup_kwargs = {
    'name': 'autoscreenshot',
    'version': '0.1.2',
    'description': '',
    'long_description': None,
    'author': 'Zija',
    'author_email': 'zija1504@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
