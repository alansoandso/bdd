from distutils.core import setup

install_requires = ['behave']

setup(
    name='bdd',
    version='0.0.1',
    description='BDD usage report',
    author='Alan So',
    author_email='alansoandso@gmail.com',
    packages=[''],
    scripts=['bdd'],
    install_requires=install_requires
)
