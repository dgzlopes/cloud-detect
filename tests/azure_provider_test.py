import pytest   # noqa: F401

from cloud_detect.providers import AzureProvider


def test_reading_correct_vendor_file():
    provider = AzureProvider()
    provider.vendor_file = 'tests/provider_files/azure'
    assert provider.check_vendor_file() is True


def test_reading_invalid_vendor_file():
    provider = AzureProvider()
    provider.vendor_file = 'tests/provider_files/aws'
    assert provider.check_vendor_file() is False
    provider.vendor_file = ''
    assert provider.check_vendor_file() is False


@pytest.mark.asyncio
async def test_valid_metadata_server_check(aresponses):
    mock_host = 'testing_metadata_url.com'
    aresponses.add(
        mock_host, '/', 'GET', response={ "compute": { "vmId": "2d907167-1eed-4ede-a75e-5ef04603b90d" }},
    )

    provider = AzureProvider()
    provider.metadata_url = f'https://{mock_host}'
    assert await provider.check_metadata_server() is True

@pytest.mark.asyncio
async def test_invalid_metadata_server_check(aresponses):
    mock_host = 'testing_metadata_url.com'
    aresponses.add(
        mock_host, '/', 'GET', response={},
    )

    provider = AzureProvider()
    provider.metadata_url = f'https://{mock_host}'
    assert await provider.check_metadata_server() is False
