import pytest   # noqa: F401

from cloud_detect.providers import AlibabaProvider


def test_reading_correct_vendor_file():
    provider = AlibabaProvider()
    provider.vendor_file = 'tests/provider_files/alibaba'
    assert provider.check_vendor_file() is True


def test_reading_invalid_vendor_file():
    provider = AlibabaProvider()
    provider.vendor_file = 'tests/provider_files/gcp'
    assert provider.check_vendor_file() is False
    provider.vendor_file = ''
    assert provider.check_vendor_file() is False


@pytest.mark.asyncio
async def test_valid_metadata_server_check(aresponses):
    mock_host = 'testing_metadata_url.com'
    aresponses.add(
        mock_host, '/', 'GET',
        aresponses.Response(text='ECS Virt', status=200),
    )
    provider = AlibabaProvider()
    provider.metadata_url = f'https://{mock_host}'
    assert await provider.check_metadata_server() is True

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_invalid_metadata_server_check(aresponses):
    mock_host = 'testing_metadata_url.com'
    aresponses.add(mock_host, '/', 'GET', aresponses.Response(text=''))
    provider = AlibabaProvider()
    provider.metadata_url = f'https://{mock_host}'
    assert await provider.check_metadata_server() is False
