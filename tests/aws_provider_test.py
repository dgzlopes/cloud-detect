import pytest   # noqa: F401

from cloud_detect.providers import AWSProvider


def test_reading_correct_vendor_file_product_version():
    provider = AWSProvider()
    provider.vendor_files = ('tests/provider_files/aws_product_version',)
    assert provider.check_vendor_file() is True


def test_reading_correct_vendor_file_bios_vendor():
    provider = AWSProvider()
    provider.vendor_files = ('tests/provider_files/aws_bios_vendor',)
    assert provider.check_vendor_file() is True


def test_reading_invalid_vendor_file():
    provider = AWSProvider()
    provider.vendor_file = 'tests/provider_files/gcp'
    assert provider.check_vendor_file() is False
    provider.vendor_file = ''
    assert provider.check_vendor_file() is False


@pytest.mark.asyncio
async def test_valid_metadata_server_check(aresponses):
    mock_host = 'testing_metadata_url.com'
    aresponses.add(
        mock_host, '/', 'GET',
        response={'imageId': 'ami-12312412', 'instanceId': 'i-ec12as'},
    )

    provider = AWSProvider()
    provider.metadata_url = f'https://{mock_host}'
    provider.metadata_token_url = f'https://{mock_host}'
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
    provider.metadata_token_url = f'https://{mock_host}'
    assert await provider.check_metadata_server() is False


@pytest.mark.asyncio
async def test_valid_metadata_server_check_v2(aresponses):
    mock_host = 'testing_metadata_url.com'
    aresponses.add(
        mock_host, '/', 'GET',
        aresponses.Response(status=401),
    )
    aresponses.add(
        mock_host, '/', 'PUT',
        response='token',
    )
    aresponses.add(
        mock_host, '/', 'GET',
        response={'imageId': 'ami-12312412', 'instanceId': 'i-ec12as'},
    )

    provider = AWSProvider()
    provider.metadata_url = f'https://{mock_host}'
    provider.metadata_token_url = f'https://{mock_host}'
    assert await provider.check_metadata_server() is True
