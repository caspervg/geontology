from distutils.core import setup
from setuptools import find_packages

setup(
    name='geontology',
    version='0.5.2',
    packages=find_packages(exclude=["tests"]),
    url='http://github.com/caspervg/geontology',
    license='MIT',
    author='Casper Van Gheluwe',
    author_email='casper.vangheluwe@ugent.be',
    description='Support library for easier access to the GeoData ontology',
    install_requires=['rdflib'],
    keywords="geodata geo ontology rdf rdflib"
)
