import asyncio
import logging
import contextlib
from pathlib import Path

import aiohttp

from . import AbstractProvider


class AWSProvider(AbstractProvider):
    """
        Concrete implementation of the AWS cloud provider.
    """
    identifier = 'aws'

    def __init__(self, logger=None):
        self.logger = logger or logging.getLogger(__name__)
        self.metadata_url = (
            'http://169.254.169.254/latest/dynamic/instance-identity/document'
        )
        self.metadata_token_url = (
            'http://169.254.169.254/latest/api/token'
        )
        self.vendor_files = (
            '/sys/class/dmi/id/product_version', '/sys/class/dmi/id/bios_vendor'
        )

    async def identify(self):
        """
            Tries to identify AWS using all the implemented options
        """
        self.logger.info('Try to identify AWS')
        return self.check_vendor_file() or await self.check_metadata_server()

    async def _get_metadata_v2(self):
        with contextlib.suppress(BaseException):
            async with aiohttp.ClientSession() as session:
                async with session.put(self.metadata_token_url, headers={'X-aws-ec2-metadata-token-ttl-seconds': '60'}) as response:
                    token = await response.text()
            return await self._get_metadata(headers={'X-aws-ec2-metadata-token': token})
        return False

    async def _get_metadata(self, headers=None):
        with contextlib.suppress(BaseException):
            async with aiohttp.ClientSession() as session:
                async with session.get(self.metadata_url, headers=headers) as response:
                    response = await response.json(content_type=None)
                    if response['imageId'].startswith('ami-', ) and response[
                        'instanceId'
                    ].startswith('i-'):
                        return True
        return False

    async def check_metadata_server(self):
        """
            Tries to identify AWS via metadata server
        """
        self.logger.debug('Checking AWS metadata')
        results = await asyncio.gather(
            self._get_metadata(),
            self._get_metadata_v2()
        )
        return any(results)

    def check_vendor_file(self):
        """
            Tries to identify AWS provider by reading the /sys/class/dmi/id/product_version
        """
        self.logger.debug('Checking AWS vendor file')
        for vendor_file in self.vendor_files:
            aws_path = Path(vendor_file)
            if aws_path.is_file():
                if 'amazon' in aws_path.read_text().lower():
                    return True
        return False
