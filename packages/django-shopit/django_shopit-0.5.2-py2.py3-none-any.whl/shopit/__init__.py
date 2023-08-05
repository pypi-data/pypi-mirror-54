# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

"""
Release logic:
 1. Bump the __version__.
 2. git add shopit/__init__.py
 3. git commit -m 'Bump to <version>'
 4. git push
 5. Make sure all tests pass on https://travis-ci.com/dinoperovic/django-shopit
 6. git tag <version>
 7. git push --tags
 8. python setup.py sdist bdist_wheel
 9. twine upload dist/*
10. Done!
"""
__version__ = '0.5.2'

default_app_config = 'shopit.apps.ShopitConfig'
