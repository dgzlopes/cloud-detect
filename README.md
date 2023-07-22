# cloud-detect
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/cloud-detect.svg)](https://pypi.org/project/cloud-detect/)
[![PyPI](https://img.shields.io/pypi/v/cloud-detect.svg)](https://pypi.org/project/cloud-detect/)
[![PyPI - License](https://img.shields.io/pypi/l/cloud-detect.svg)](https://github.com/dgzlopes/cloud-detect/blob/master/LICENSE.md)
[![Build Status](https://github.com/dgzlopes/cloud-detect/workflows/Testing%20for%20Python%20Versions%203.6-3.11%20via%20tox/badge.svg)](https://github.com/dgzlopes/cloud-detect/actions?query=workflow%3A%22Testing+for+Python+Versions+3.6-3.11+via+tox%22)

## About
`cloud-detect` is a Python module that determines a host's cloud provider. Highly inspired by the Go based [Satellite](https://github.com/banzaicloud/satellite), `cloud-detect` uses the same techniques (file systems and provider metadata) to properly identify cloud providers.

## Features
- Supports identification of Alibaba, AWS, Azure, Digital Ocean, GCP and Oracle Cloud hosts.
- Fast and supports asyncio
- Logging integration.
- Small and extensible.

## Usage

```
>>> from cloud_detect import provider
>>> provider()
'aws'

>>> provider() # when tested in local/non-supported cloud env
'unknown'
```

> Right now the only possible responses are: 'alibaba', 'aws', 'azure', 'do', 'gcp', 'oci' or 'unknown'

> You can get the list of supported providers using
>>`>>> from cloud_detect import SUPPORTED_PROVIDERS`

## Installation
Via pip:
```
pip install cloud-detect
```

## Examples
[Termination-handler](https://github.com/dgzlopes/termination-handler) uses cloud-detect to keep the handling of termination notices on spot/preemptible instances cloud-agnostic, making easier to operate the same tooling in various distinct environments.

## How to contribute
1. Check for open issues or open a fresh issue to start a discussion around a feature idea or a bug.
2. Fork [the repository](https://github.com/dgzlopes/cloud-detect) on GitHub to start making your changes to the master branch (or branch off of it).
3. Write a test which shows that the bug was fixed or that the feature works as expected.
4. Send a [pull request](https://help.github.com/en/articles/creating-a-pull-request-from-a-fork) and bug [me](https://github.com/dgzlopes) until it gets merged and published.

Some things that would be great to have:
- Add cloud providers (Vultr)
- Add codecov
