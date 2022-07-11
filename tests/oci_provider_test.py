from cloud_detect.providers import OCIProvider


def test_reading_correct_vendor_file():
    provider = OCIProvider()
    provider.vendor_file = 'tests/provider_files/oci'
    assert provider.check_vendor_file() is True


def test_reading_invalid_vendor_file():
    provider = OCIProvider()
    assert provider.check_vendor_file('tests/provider_files/gcp') is False
    assert provider.check_vendor_file('') is False
