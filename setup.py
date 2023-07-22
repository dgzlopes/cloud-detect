from sys import version_info as py_version

import setuptools
from distutils.core import setup

long_description = ''
try:
    with open('README.md') as f:
        long_description = f.read()
except FileNotFoundError:
    pass

if py_version.minor >= 7:
    install_requires = ['aiohttp>=3.7']
else:
    install_requires = ['aiohttp>=3.7,<4']

setup(
    name='cloud-detect',
    version='0.0.11',
    description="Module that determines a host's cloud provider",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/dgzlopes/cloud-detect',
    license='MIT',
    install_requires=install_requires,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Systems Administration',
        'Topic :: System :: Networking',
    ],
    python_requires='>=3.6',
    author='Daniel Gonzalez Lopes',
    author_email='danielgonzalezlopes@gmail.com',
    packages=setuptools.find_packages(),
)
