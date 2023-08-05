from setuptools import find_packages, setup
import sys

requirements = [
    'numpy',
    'scipy',
    'pandas',
    'pyspark'
]

#public version 0.0.4
version = '0.0.4'

setup(
    name='search-tools',
    version=version,
    author="Michael Klear",
    author_email='fixityourself@fu.com',
    url='https://github.com/AlliedToasters/search-tools/archive/v0.0.4.tar.gz',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements
)
