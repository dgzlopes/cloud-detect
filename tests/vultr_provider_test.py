import pytest   # noqa: F401

from cloud_detect.providers import VultrProvider


def test_reading_correct_vendor_file():
    provider = VultrProvider()
    provider.vendor_file = 'tests/provider_files/vultr'
    assert provider.check_vendor_file() is True


def test_reading_invalid_vendor_file():
    provider = VultrProvider()
    provider.vendor_file = 'tests/provider_files/aws'
    assert provider.check_vendor_file() is False
    provider.vendor_file = ''
    assert provider.check_vendor_file() is False


@pytest.mark.asyncio
async def test_valid_metadata_server_check(aresponses):
    mock_host = 'testing_metadata_url.com'
    aresponses.add(
        mock_host, '/', 'GET', response={'instanceid': "67218358"},
    )

    provider = VultrProvider()
    provider.metadata_url = f'https://{mock_host}'
    assert await provider.check_metadata_server() is True


@pytest.mark.asyncio
async def test_invalid_metadata_server_check(aresponses):
    mock_host = 'testing_metadata_url.com'
    aresponses.add(
        mock_host, '/', 'GET', response={},
    )

    provider = VultrProvider()
    provider.metadata_url = f'https://{mock_host}'
    assert await provider.check_metadata_server() is False
