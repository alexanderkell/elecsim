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
  name = 'elecsim',         # How you named your package folder (MyLib)
  packages = find_packages(exclude=['tests', 'tests.*']),   # Chose the same as "name"
  package_data={'elecsim': extra_files},
  # package_data={'elecsim': },
  # include_package_data=True,
  py_modules=['elecsim'],
  version = '0.1.17',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Agent-based Model for Electricity Markets',   # Give a short description about your library
  author = 'Alexander Kell',                   # Type in your name
  author_email = 'alexander@kell.es',      # Type in your E-Mail
  url = 'https://github.com/alexanderkell/elecsim',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/alexanderkell/elecsim/archive/0.1.1.1.tar.gz',    # I explain this later on
  keywords = ['ElecSIM', 'Agent-based', 'Electricity', 'Market', 'Model', 'Simulation'],   # Keywords that define your package best
    install_requires=[  # I get to this in a second
        'mesa',
        'pandas',
        'scipy',
        'pytest',
        'pathos',
        'ray[rllib]',
    ],
  classifiers=[
    'Development Status :: 4 - Beta',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which python versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
  ],
)
