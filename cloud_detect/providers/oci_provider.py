import asyncio
import contextlib
import logging
from pathlib import Path

import aiohttp

from .provider import AbstractProvider


class OCIProvider(AbstractProvider):
    """
        Concrete implementation of the Oracle Cloud Infrastructure cloud provider.
    """
    identifier = 'oci'

    def __init__(self, logger=None):
        self.logger = logger or logging.getLogger(__name__)
        self.metadata_url = 'http://169.254.169.254/opc/v1/instance/'
        self.metadata_url_v2 = 'http://169.254.169.254/opc/v2/instance/'
        self.headers = {'Authorization': 'Bearer Oracle'}
        self.vendor_file = '/sys/class/dmi/id/chassis_asset_tag'

    async def identify(self):
        """
            Tries to identify OCI using all the implemented options
        """
        self.logger.info('Try to identify OCI')
        return self.check_vendor_file() or await self.check_metadata_server()

    async def _get_metadata_v2(self):
        with contextlib.suppress(BaseException):
            return await self._get_metadata(url=self.metadata_url_v2, headers=self.headers)
        return False

    async def _get_metadata(self, url=None, headers=None):
        with contextlib.suppress(BaseException):
            async with aiohttp.ClientSession() as session:
                async with session.get(url or self.metadata_url, headers=headers) as response:
                    response = await response.json(content_type=None)
                    if str(response.get('id', '')).startswith('ocid1.instance.'):
                        return True
        return False

    async def check_metadata_server(self):
        """
            Tries to identify OCI via metadata server
        """
        self.logger.debug('Checking OCI metadata')
        results = await asyncio.gather(
            self._get_metadata(),
            self._get_metadata_v2(),
        )
        return any(results)

    def check_vendor_file(self):
        """
            Tries to identify OCI provider by reading the file
            /sys/class/dmi/id/chassis_asset_tag
        """
        self.logger.debug('Checking OCI vendor file')
        oci_path = Path(self.vendor_file)
        if oci_path.is_file():
            if 'OracleCloud' in oci_path.read_text():
                return True
        return False
