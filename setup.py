#!/usr/bin/env python

from setuptools import setup

setup(name='adjutant',
      version='0.1.2',
      author='Aku Kotkavuo',
      author_email='aku@hibana.net',
      url='http://github.com/arkx/adjutant/',
      description='A Python library for parsing StarCraft II replays.',
      py_modules=['adjutant'],
      requires=['mpyq'],
      install_requires=['mpyq'],
      entry_points={
        'console_scripts': ['adjutant = adjutant:main']
      },
      classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 2.7',
        'Topic :: Games/Entertainment :: Real Time Strategy',
        'Topic :: Software Development :: Libraries',
      ],
     )
