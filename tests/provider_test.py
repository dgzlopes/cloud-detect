import asyncio

import pytest   # noqa: F401

import cloud_detect
from cloud_detect.providers import AbstractProvider


def test_supported_providers():
    assert cloud_detect.SUPPORTED_PROVIDERS == \
        ('alibaba', 'aws', 'azure', 'do', 'gcp', 'oci')


def test_provider(monkeypatch):
    async def mockreturn(t):
        return 'cloudy'

    monkeypatch.setattr(cloud_detect, '_identify', mockreturn)

    assert cloud_detect.provider() == 'cloudy'


@pytest.mark.asyncio
async def test_async_provider(monkeypatch):
    async def mockreturn(t):
        return 'cloudy'

    monkeypatch.setattr(cloud_detect, '_identify', mockreturn)

    assert await cloud_detect.async_provider() == 'cloudy'


class BaseTestProviderClass(AbstractProvider):

    def __init__(self, logger=None):
        self.server_response = None
        self.file_response = None
        self.delay = None

    async def identify(self):
        return self.check_vendor_file() or await self.check_metadata_server()

    async def check_metadata_server(self):
        await asyncio.sleep(self.delay)
        return self.server_response

    def check_vendor_file(self):
        return self.file_response


def create_test_provider_class(name, server_response=True, file_respone=True, delay=0.25):
    class TPC(BaseTestProviderClass):
        identifier = name

        def __init__(self, logger=None):
            self.server_response = server_response
            self.file_response = file_respone
            self.delay = delay

    return TPC


@pytest.mark.asyncio
async def test_identify(monkeypatch):
    mock_pcs = []
    for args in [('c1', True, True), ('c2', False, False)]:
        mock_pcs.append(create_test_provider_class(*args))

    monkeypatch.setattr(cloud_detect, '__PROVIDER_CLASSES', mock_pcs)

    assert await cloud_detect._identify(0.5) == 'c1'


@pytest.mark.asyncio
async def test_identify_assertion_error():
    timeout = 0.01
    with pytest.raises(
        AssertionError,
        match=f'`timeout` should be a number and > 0.1, provided value: {timeout}',
    ):
        await cloud_detect._identify(timeout)

    timeout = '0'
    with pytest.raises(
        AssertionError,
        match=f'`timeout` should be a number and > 0.1, provided value: {timeout}',
    ):
        await cloud_detect._identify(timeout)


@pytest.mark.asyncio
async def test_identify_timeout(monkeypatch):
    mock_pcs = []
    for args in [('c1', False, False, 1), ('c2', False, False, 3)]:
        mock_pcs.append(create_test_provider_class(*args))

    monkeypatch.setattr(cloud_detect, '__PROVIDER_CLASSES', mock_pcs)

    assert await cloud_detect._identify(0.5) == 'unknown'


@pytest.mark.asyncio
async def test_identify_unknown(monkeypatch):
    mock_pcs = []
    for args in [('c1', False, False, 0.2), ('c2', False, False, 0.2)]:
        mock_pcs.append(create_test_provider_class(*args))

    monkeypatch.setattr(cloud_detect, '__PROVIDER_CLASSES', mock_pcs)

    assert await cloud_detect._identify(0.5) == 'unknown'
