import logging

from cloud_detect.providers import AlibabaProvider
from cloud_detect.providers import AWSProvider
from cloud_detect.providers import AzureProvider
from cloud_detect.providers import DOProvider
from cloud_detect.providers import GCPProvider


def provider(excluded=[]):
    if 'alibaba' not in excluded and AlibabaProvider.identify():
        logging.debug('Cloud_detect result is alibaba')
        return 'alibaba'
    elif 'aws' not in excluded and AWSProvider().identify():
        logging.debug('Cloud_detect result is aws')
        return 'aws'
    elif 'gcp' not in excluded and GCPProvider().identify():
        logging.debug('Cloud_detect result is gcp')
        return 'gcp'
    elif 'do' not in excluded and DOProvider().identify():
        logging.debug('Cloud_detect result is do')
        return 'do'
    elif 'azure' not in excluded and AzureProvider().identify():
        logging.debug('Cloud_detect result is azure')
        return 'azure'
    else:
        logging.debug('Cloud_detect result is unknown')
        return 'unknown'
