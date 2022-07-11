import logging
from pathlib import Path

import aiohttp

from . import AbstractProvider


class GCPProvider(AbstractProvider):
    """
        Concrete implementation of the GCP cloud provider.
    """
    identifier = 'gcp'

    def __init__(self, logger=None):
        self.logger = logger or logging.getLogger(__name__)
        self.metadata_url = (
            'http://metadata.google.internal/computeMetadata/v1/instance/tags'
        )
        self.vendor_file = '/sys/class/dmi/id/product_name'
        self.headers = {'Metadata-Flavor': 'Google'}

    async def identify(self):
        """
            Tries to identify GCP using all the implemented options
        """
        self.logger.info('Try to identify GCP')
        return self.check_vendor_file() or await self.check_metadata_server()

    async def check_metadata_server(self):
        """
            Tries to identify GCP via metadata server
        """
        self.logger.debug('Checking GCP metadata')
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.metadata_url):
                    return True
        except aiohttp.ClientError as e:  # noqa: F841
            return False

    def check_vendor_file(self):
        """
            Tries to identify GCP provider by reading the /sys/class/dmi/id/product_name
        """
        self.logger.debug('Checking GCP vendor file')
        gcp_path = Path(self.vendor_file)
        if gcp_path.is_file():
            if 'Google' in gcp_path.read_text():
                return True
        return False
