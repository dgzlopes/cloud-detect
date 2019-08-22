import logging

from cloud_detect.providers import AWSProvider
from cloud_detect.providers import DOProvider
from cloud_detect.providers import GCPProvider


def provider(excluded=[]):
    if 'aws' not in excluded and AWSProvider().identify():
        logging.debug('Cloud_detect result is aws')
        return 'aws'
    elif 'gcp' not in excluded and GCPProvider().identify():
        logging.debug('Cloud_detect result is gcp')
        return 'gcp'
    elif 'do' not in excluded and DOProvider().identify():
        logging.debug('Cloud_detect result is do')
        return 'do'
    else:
        logging.debug('Cloud_detect result is unknown')
        return 'unknown'
