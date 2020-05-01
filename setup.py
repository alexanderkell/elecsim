from distutils.core import setup
from setuptools import find_packages

import os

def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join('..', path, filename))
    return paths

extra_files = package_files('elecsim/data/processed/')
print(extra_files)

setup(
  name = 'elecsim',
  packages = find_packages(exclude=['tests*', 'tests.*']),
  package_data={'elecsim': extra_files},

  py_modules=['elecsim'],
  version = '0.1.78',
  license='MIT',
  description = 'Agent-based Model for Electricity Markets',
  author = 'Alexander Kell',
  author_email = 'alexander@kell.es',
  url = 'https://github.com/alexanderkell/elecsim',
  download_url = 'https://github.com/alexanderkell/elecsim/archive/0.1.1.1.tar.gz',
  keywords = ['ElecSIM', 'Agent-based', 'Electricity', 'Market', 'Model', 'Simulation'],
    install_requires=[
        'mesa',
        'pandas',
        'scipy',
        'pathos'
    ],
  classifiers=[
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
  ],
)
