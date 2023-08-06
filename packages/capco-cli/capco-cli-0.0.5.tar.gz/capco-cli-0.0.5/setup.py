import os

from setuptools import setup, find_packages


def read(filename):
    with open(os.path.join(os.path.dirname(__file__), filename)) as f:
        return f.read()


setup(
    name='capco-cli',
    version=read('VERSION'),
    packages=find_packages(exclude=['tests']),
    url='https://bitbucket.org/ilabs-capco/capco-cli',
    author='Capco UK',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    python_requires='>=3.7',
    install_requires=read('requirements.txt').splitlines(),
    entry_points={
        'console_scripts': [
            'capco = src.__main__:main'
        ]
    }
)
