#!/usr/bin/env python

from setuptools import setup, find_packages

VERSION = '0.0.1'
LONG_DESC = """\
A python wrapper to the USPS api, currently only supports the address information api
"""

setup(name='python-usps',
      version=VERSION,
      description="A python wrapper to the USPS api, currently only supports the address information api",
      long_description=LONG_DESC,
      classifiers=[
          'Programming Language :: Python',
          'Operating System :: OS Independent',
          'Natural Language :: English',
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
      ],
      keywords='usps api shipping',
      author='Jason Kraus',
      author_email='zbyte64@gmail.com',
      maintainer = 'Jason Kraus',
      maintainer_email = 'zbyte64@gmail.com',
      url='http://github.com/cuker/python-usps',
      license='New BSD License',
      packages=find_packages(exclude=['ez_setup', 'usps', 'tests']),
      zip_safe=False,
      install_requires=[
      ],
      #test_suite='tests.test_suite',
      )
