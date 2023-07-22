import logging
from pathlib import Path

import aiohttp

from . import AbstractProvider


class VultrProvider(AbstractProvider):
    """
        Concrete implementation of the Vultr cloud provider.
    """
    identifier = 'vultr'

    def __init__(self, logger=None):
        self.logger = logger or logging.getLogger(__name__)
        self.metadata_url = 'http://169.254.169.254/v1.json'
        self.vendor_file = '/sys/class/dmi/id/sys_vendor'

    async def identify(self):
        """
            Tries to identify Vultr using all the implemented options
        """
        self.logger.info('Try to identify Vultr')
        return self.check_vendor_file() or await self.check_metadata_server()

    async def check_metadata_server(self):
        """
            Tries to identify Vultr via metadata server
        """
        self.logger.debug('Checking Vultr metadata')
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.metadata_url) as response:
                    response = await response.json()
                    return len(response['instanceid']) > 0
        except BaseException:
            return False

    def check_vendor_file(self):
        """
            Tries to identify Vultr provider by reading the /sys/class/dmi/id/sys_vendor
        """
        self.logger.debug('Checking Vultr vendor file')
        vendor_path = Path(self.vendor_file)
        return vendor_path.is_file() and 'Vultr' in vendor_path.read_text()
