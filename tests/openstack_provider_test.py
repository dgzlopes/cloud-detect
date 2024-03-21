import pytest   # noqa: F401

from cloud_detect.providers import OpenStackProvider


def test_reading_correct_vendor_file_product_name():
    provider = OpenStackProvider()
    provider.vendor_files = ('tests/provider_files/openstack_product_name',)
    assert provider.check_vendor_file() is True


def test_reading_correct_vendor_file_chassis_asset_tag():
    provider = OpenStackProvider()
    provider.vendor_files = ('tests/provider_files/openstack_chassis_asset_tag',)
    assert provider.check_vendor_file() is True


def test_reading_invalid_vendor_file():
    provider = OpenStackProvider()
    provider.vendor_files = ('tests/provider_files/gcp',)
    assert provider.check_vendor_file() is False
    provider.vendor_files = ('',)
    assert provider.check_vendor_file() is False


@pytest.mark.asyncio
async def test_valid_metadata_server_check(aresponses):
    mock_host = 'testing_metadata_url.com'
    aresponses.add(
        mock_host, '/', 'GET', response={},
    )

    provider = OpenStackProvider()
    provider.metadata_url = f'https://{mock_host}'
    assert await provider.check_metadata_server() is True


@pytest.mark.asyncio
async def test_invalid_metadata_server_check(aresponses):
    mock_host = 'testing_metadata_url.com'
    aresponses.add(
        mock_host, '/', 'GET', aresponses.Response(text='error', status=404),
    )

    provider = OpenStackProvider()
    provider.metadata_url = f'https://{mock_host}'
    assert await provider.check_metadata_server() is False
