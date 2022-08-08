import logging
from pathlib import Path

import aiohttp

from . import AbstractProvider


class DOProvider(AbstractProvider):
    """
        Concrete implementation of the Digital Ocean cloud provider.
    """
    identifier = 'do'

    def __init__(self, logger=None):
        self.logger = logger or logging.getLogger(__name__)
        self.metadata_url = 'http://169.254.169.254/metadata/v1.json'
        self.vendor_file = '/sys/class/dmi/id/sys_vendor'

    async def identify(self):
        """
            Tries to identify DO using all the implemented options
        """
        self.logger.info('Try to identify DO')
        return self.check_vendor_file() or await self.check_metadata_server()

    async def check_metadata_server(self):
        """
            Tries to identify DO via metadata server
        """
        self.logger.debug('Checking DO metadata')
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.metadata_url) as response:
                    response = await response.json()
                    return response['droplet_id'] > 0
        except BaseException:
            return False

    def check_vendor_file(self):
        """
            Tries to identify DO provider by reading the /sys/class/dmi/id/sys_vendor
        """
        self.logger.debug('Checking DO vendor file')
        do_path = Path(self.vendor_file)
        if do_path.is_file():
            if 'DigitalOcean' in do_path.read_text():
                return True
        return False
