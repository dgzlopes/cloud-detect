import pytest   # noqa: F401

from cloud_detect.providers import AWSProvider


def test_reading_correct_vendor_file():
    provider = AWSProvider()
    assert provider.check_vendor_file('tests/provider_files/aws') is True
    assert provider.check_vendor_file('tests/provider_files/aws2') is True


def test_reading_invalid_vendor_file():
    provider = AWSProvider()
    assert provider.check_vendor_file('tests/provider_files/gcp') is False
    assert provider.check_vendor_file('') is False


@pytest.mark.asyncio
async def test_valid_metadata_server_check(aresponses):
    mock_host = 'testing_metadata_url.com'
    aresponses.add(
        mock_host, '/', 'GET',
        response={'imageId': 'ami-12312412', 'instanceId': 'i-ec12as'},
    )

    provider = AWSProvider()
    provider.metadata_url = f'https://{mock_host}'
    assert await provider.check_metadata_server() is True


@pytest.mark.asyncio
async def test_invalid_metadata_server_check(aresponses):
    mock_host = 'testing_metadata_url.com'
    aresponses.add(
        mock_host, '/', 'GET',
        response={'imageId': 'some_ID', 'instanceId': 'some_Instance'},
    )

    provider = AWSProvider()
    provider.metadata_url = f'https://{mock_host}'
    assert await provider.check_metadata_server() is False
