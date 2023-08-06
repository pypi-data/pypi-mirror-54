# -*- coding: utf-8 -*-
from distutils.core import setup

modules = \
['pixelmatch']
setup_kwargs = {
    'name': 'pixelmatch',
    'version': '0.1.0',
    'description': 'A pixel-level image comparison library. Python port of https://github.com/mapbox/pixelmatch',
    'long_description': None,
    'author': 'Wu Haotian',
    'author_email': 'whtsky@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
