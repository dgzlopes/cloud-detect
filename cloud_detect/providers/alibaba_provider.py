import logging
from pathlib import Path

import aiohttp

from . import AbstractProvider


class AlibabaProvider(AbstractProvider):
    """
        Concrete implementation of the AWS cloud provider.
    """
    identifier = 'alibaba'

    def __init__(self, logger=None):
        self.logger = logger or logging.getLogger(__name__)
        self.metadata_url = 'http://100.100.100.200/latest/meta-data/latest/meta-data/instance/virtualization-solution'  # noqa
        self.vendor_file = '/sys/class/dmi/id/product_name'

    async def identify(self):
        """
            Tries to identify Alibaba using all the implemented options
        """
        self.logger.info('Try to identify Alibaba')
        return self.check_vendor_file() or await self.check_metadata_server()

    async def check_metadata_server(self):
        """
            Tries to identify Alibaba via metadata server
        """
        self.logger.debug('Checking Alibaba metadata')
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.metadata_url) as response:
                    return await response.text() == 'ECS Virt'
        except BaseException:
            return False

    def check_vendor_file(self):
        """
            Tries to identify Alibaba provider by reading the /sys/class/dmi/id/product_name
        """
        self.logger.debug('Checking Alibaba vendor file')
        alibaba_path = Path(self.vendor_file)
        if alibaba_path.is_file():
            if 'Alibaba Cloud ECS' in alibaba_path.read_text():
                return True
        return False
