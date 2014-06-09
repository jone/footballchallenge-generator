from setuptools import setup, find_packages


setup(name='wm2012',
      packages=find_packages(exclude=['ez_setup']),
      install_requires=[
        'ftw.testbrowser',
        'setuptools',
        'zope.interface',
        'lxml<=2.3.6',
        'path.py',
        ],

      entry_points = {
        'console_scripts': [
            'generate = wm2012.generator:command',
            'fetch = wm2012.fetch:command']
        },
      )
