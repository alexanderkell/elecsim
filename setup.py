from setuptools import setup

setup(
    name='elecsim',
    version='1.0',
    description='A package for simulating the impact of technology and policy on the electricity sector',
    author='Alexander Kell',
    author_email='alexander@kell.es',
    url='https://github.com/alexanderkell/elecsim',
    packages=['elecsim'],
    install_requires=['mesa'], # external packages as dependencies
    long_description="A package to aid in the designing of an energy market of a country to see impacts of different regulatory and technological changes",
)
