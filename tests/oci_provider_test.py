import pytest

from cloud_detect.providers import OCIProvider


def test_reading_correct_vendor_file():
    provider = OCIProvider()
    provider.vendor_file = 'tests/provider_files/oci'
    assert provider.check_vendor_file() is True


def test_reading_invalid_vendor_file():
    provider = OCIProvider()
    provider.vendor_file = 'tests/provider_files/gcp'
    assert provider.check_vendor_file() is False
    provider.vendor_file = ''
    assert provider.check_vendor_file() is False


@pytest.mark.asyncio
async def test_valid_metadata_server_check(aresponses):
    mock_host = 'testing_metadata_url.com'
    aresponses.add(
        mock_host, '/', 'GET',
        response={'id': 'ocid1.instance.oc1.phx.abc', 'region': 'phx'},
    )
    aresponses.add(
        mock_host, '/', 'GET',
        response={'id': 'ocid1.instance.oc1.phx.abc', 'region': 'phx'},
    )

    provider = OCIProvider()
    provider.metadata_url = f'https://{mock_host}'
    provider.metadata_url_v2 = f'https://{mock_host}'
    assert await provider.check_metadata_server() is True


@pytest.mark.asyncio
async def test_invalid_metadata_server_check(aresponses):
    mock_host = 'testing_metadata_url.com'
    aresponses.add(
        mock_host, '/', 'GET',
        response={'id': 'i-notoracle', 'region': 'somewhere'},
    )
    aresponses.add(
        mock_host, '/', 'GET',
        response={'id': 'i-notoracle', 'region': 'somewhere'},
    )

    provider = OCIProvider()
    provider.metadata_url = f'https://{mock_host}'
    provider.metadata_url_v2 = f'https://{mock_host}'
    assert await provider.check_metadata_server() is False
