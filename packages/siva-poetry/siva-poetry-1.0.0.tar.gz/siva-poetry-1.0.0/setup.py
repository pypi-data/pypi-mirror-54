# -*- coding: utf-8 -*-
from distutils.core import setup

package_dir = \
{'': 'src'}

packages = \
['siva_poetry']

package_data = \
{'': ['*'], 'siva_poetry': ['config/*']}

install_requires = \
['pendulum>=2.0,<3.0', 'pyyaml>=5.1,<6.0']

entry_points = \
{'console_scripts': ['start_pendulum = siva_poetry:get_time']}

setup_kwargs = {
    'name': 'siva-poetry',
    'version': '1.0.0',
    'description': 'Simple project',
    'long_description': None,
    'author': 'siva',
    'author_email': 'sivakon@outlook.com',
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
