import pytest   # noqa: F401
import requests   # noqa: F401
import responses   # noqa: F401

from cloud_detect.providers import GCPProvider


def test_reading_correct_vendor_file():
    provider = GCPProvider()
    provider.vendor_file = 'tests/provider_files/gcp'
    assert provider.check_vendor_file() is True


def test_reading_invalid_vendor_file():
    provider = GCPProvider()
    provider.vendor_file = 'tests/provider_files/aws'
    assert provider.check_vendor_file() is False
    provider.vendor_file = ''
    assert provider.check_vendor_file() is False


@responses.activate
def test_invalid_metadata_server_check():
    mocking_url = 'http://testing_metadata_url.com'
    responses.add(
        responses.GET, 'http://testing_metadata_url.com',
        json={},
    )

    provider = GCPProvider()
    provider.metadata_url = mocking_url
    assert provider.check_metadata_server() is True
