# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['openlaw']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'openlaw',
    'version': '0.1.1',
    'description': 'A metapackage for OpenLaw Israel projects',
    'long_description': None,
    'author': 'Yehuda Deutsch',
    'author_email': 'yeh@uda.co.il',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
