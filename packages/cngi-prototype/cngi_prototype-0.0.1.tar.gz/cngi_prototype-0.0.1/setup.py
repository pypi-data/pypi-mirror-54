from setuptools import setup, find_packages
import os
import sys

with open('README.md', encoding='utf-8') as fid:
    long_description = fid.read()

setup(
    name='cngi_prototype',
    version='0.0.1',
    description='casa next generation infrastructure prototype',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='National Radio Astronomy Observatory',
    author_email='casa-feedback@nrao.edu',
    url='https://github.com/casangi/cngi_prototype',
    license='Apache-2.0',
    packages=find_packages(),
    install_requires=['numpy>=1.17.3',
                      'dask>=2.6.0',
                      'distributed>=2.6.0',
                      'pyarrow>=0.15.0',
                      'bokeh>=1.3.4',
                      'pandas>=0.25.2'],
)
