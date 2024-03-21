import logging
from pathlib import Path

import aiohttp

from . import AbstractProvider


class OpenStackProvider(AbstractProvider):
    """
        Concrete implementation of the OpenStack cloud provider.
    """
    identifier = 'openstack'

    def __init__(self, logger=None):
        self.logger = logger or logging.getLogger(__name__)
        self.metadata_url = 'http://169.254.169.254/openstack'
        self.vendor_files = (
            '/sys/class/dmi/id/product_name',
            '/sys/class/dmi/id/chassis_asset_tag',
        )

    async def identify(self):
        """
            Tries to identify OpenStack using all the implemented options
        """
        self.logger.info('Try to identify OpenStack')
        return self.check_vendor_file() or await self.check_metadata_server()

    async def check_metadata_server(self):
        """
            Tries to identify OpenStack via metadata server
        """
        self.logger.debug('Checking OpenStack metadata')
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.metadata_url) as response:
                    return response.status == 200
        except aiohttp.ClientError as e:  # noqa: F841
            return False

    def check_vendor_file(self):
        """
            Tries to identify OpenStack provider by reading the /sys/class/dmi/id/product_name
        """
        self.logger.debug('Checking OpenStack vendor file')
        for vendor_file in self.vendor_files:
            openstack_path = Path(vendor_file)
            if openstack_path.is_file():
                if any(name in openstack_path.read_text() for name in (
                    "Openstack Nova",
                    "OpenStack Compute",
                    "HUAWEICLOUD",
                    "OpenTelekomCloud",
                    "SAP CCloud VM",
                    "OpenStack Nova",
                )):
                    return True
        return False
