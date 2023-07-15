import logging
from pathlib import Path

import aiohttp

from . import AbstractProvider


class AzureProvider(AbstractProvider):
    """
        Concrete implementation of the Azure cloud provider.
    """
    identifier = 'azure'

    def __init__(self, logger=None):
        self.logger = logger or logging.getLogger(__name__)
        self.metadata_url = (
            'http://169.254.169.254/metadata/instance?api-version=2017-12-01'
        )
        self.vendor_file = '/sys/class/dmi/id/sys_vendor'
        self.headers = {'Metadata': 'true'}

    async def identify(self):
        """
            Tries to identify Azure using all the implemented options
        """
        self.logger.info('Try to identify Azure')
        return self.check_vendor_file() or await self.check_metadata_server()

    async def check_metadata_server(self):
        """
            Tries to identify Azure via metadata server
        """
        self.logger.debug('Checking Azure metadata')
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.metadata_url, headers=self.headers) as response:
                    response = await response.json()
                    return len(response['compute']['vmId']) > 0
        except BaseException:
            return False

    def check_vendor_file(self):
        """
            Tries to identify Azure provider by reading the /sys/class/dmi/id/sys_vendor
        """
        self.logger.debug('Checking Azure vendor file')
        ms_path = Path(self.vendor_file)
        if ms_path.is_file():
            if 'Microsoft Corporation' in ms_path.read_text():
                return True
        return False
