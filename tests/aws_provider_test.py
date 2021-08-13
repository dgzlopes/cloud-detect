import pytest   # noqa: F401
import requests   # noqa: F401
import responses

from cloud_detect.providers import AWSProvider


def test_reading_correct_vendor_file():
    provider = AWSProvider()
    provider.vendor_file = 'tests/provider_files/aws'
    assert provider.check_vendor_file() is True


def test_reading_invalid_vendor_file():
    provider = AWSProvider()
    provider.vendor_file = 'tests/provider_files/gcp'
    assert provider.check_vendor_file() is False
    provider.vendor_file = ''
    assert provider.check_vendor_file() is False


@responses.activate
def test_valid_metadata_server_check():
    mocking_url = 'http://testing_metadata_url.com'
    responses.add(
        responses.GET, 'http://testing_metadata_url.com',
        json={'imageID': 'ami-12312412', 'instanceId': 'i-ec12as'},
    )

    provider = AWSProvider()
    provider.metadata_url = mocking_url
    assert provider.check_metadata_server() is True


@responses.activate
def test_invalid_metadata_server_check():
    mocking_url = 'http://testing_metadata_url.com'
    responses.add(
        responses.GET, 'http://testing_metadata_url.com',
        json={'imageID': 'some_ID', 'instanceId': 'some_Instance'},
    )

    provider = AWSProvider()
    provider.metadata_url = mocking_url
    assert provider.check_metadata_server() is False
