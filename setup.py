from setuptools import setup, find_packages


setup(name='wm2012',
      packages=find_packages(exclude=['ez_setup']),
      install_requires=[
        'setuptools',
        ],

      entry_points = {
        'console_scripts': [
            'generate = wm2012.generator:command']
        },
      )
