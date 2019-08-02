# cloud-detect
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/cloud-detect.svg)
![PyPI](https://img.shields.io/pypi/v/cloud-detect.svg)
![PyPI - License](https://img.shields.io/pypi/l/cloud-detect.svg)
## About
`cloud-detect` is a Python module that determines a host's cloud provider. Highly inspired by the Go based [Satellite](https://github.com/banzaicloud/satellite), `cloud-detect` uses the same techniques (file systems and provider metadata) to properly identify cloud providers.

## Features
- Supports identification of AWS and GCP hosts.
- Supports skipping providers identification.
- Logging integration.
- Small and extensible.

## Usage

```
>>> from cloud_detect import provider
>>> provider()
'aws'
>>> provider(excluded='aws')
'unknown'
```
> Right now the only possible responses are: 'aws', 'gcp' or 'unknown'
## Installation
Via pip:
```
pip install cloud-detect
```
## How to contribute
1. Check for open issues or open a fresh issue to start a discussion around a feature idea or a bug.
2. Fork [the repository](https://github.com/dgzlopes/cloud-detect) on GitHub to start making your changes to the master branch (or branch off of it).
3. Write a test which shows that the bug was fixed or that the feature works as expected.
4. Send a [pull request](https://help.github.com/en/articles/creating-a-pull-request-from-a-fork) and bug [me](https://github.com/dgzlopes) until it gets merged and published.

Some things that would be great to have:
- More cloud providers
- Add codecov
- Add automated testing and releases with CircleCI.