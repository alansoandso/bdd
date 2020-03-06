from glob import glob
from os.path import basename
from os.path import splitext

from setuptools import find_packages
from setuptools import setup

install_requires = [
    'behave',
    'pytest-bdd'
]

setup(
    name='bdd',
    version='0.0.1',
    description='BDD usage report',
    author='Alan So',
    author_email='alansoandso@gmail.com',
    packages=['bdd'],
    include_package_data=True,
    entry_points={'console_scripts': ['bdd = bdd.tool:command_line_runner', ]},
    install_requires=install_requires
)
