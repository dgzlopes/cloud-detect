from distutils.core import setup

import setuptools

long_description = ''
try:
    with open('README.md') as f:
        long_description = f.read()
except FileNotFoundError:
    pass

setup(
    name='cloud-detect',
    version='0.0.6',
    description="Module that determines a host's cloud provider",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/dgzlopes/cloud-detect',
    license='MIT',
    install_requires=[
        'requests>=2.21.0,<3',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Systems Administration',
        'Topic :: System :: Networking',
    ],
    python_requires='>=3.4',
    author='Daniel Gonzalez Lopes',
    author_email='danielgonzalezlopes@gmail.com',
    packages=setuptools.find_packages(),
)
