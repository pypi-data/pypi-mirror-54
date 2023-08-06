# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['mdc']

package_data = \
{'': ['*'], 'mdc': ['resources/*', 'templates/*']}

entry_points = \
{'console_scripts': ['mdc = mdc.mdc:main']}

setup_kwargs = {
    'name': 'shinymdc',
    'version': '2.1.0',
    'description': 'Tool to compile markdown files to tex/pdf using pandoc, latexmk',
    'long_description': '# mdc\n\nMarkdown to tex/pdf compiler.\n',
    'author': 'Jayanth Koushik',
    'author_email': 'jnkoushik@gmail.com',
    'url': 'https://github.com/jayanthkoushik/mdc',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
