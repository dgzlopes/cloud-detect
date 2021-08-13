import logging
from pathlib import Path

from . import AbstractProvider


class OCIProvider(AbstractProvider):
    """
        Concrete implementation of the Oracle Cloud Infrastructure cloud provider.
    """

    def __init__(self, logger=None):
        self.logger = logger or logging.getLogger(__name__)
        self.vendor_file = '/sys/class/dmi/id/chassis_asset_tag'

    def identify(self):
        """
            Tries to identify OCI using all the implemented options
        """
        self.logger.info('Try to identify OCI')
        return self.check_vendor_file()

    def check_metadata_server(self):
        raise NotImplementedError

    def check_vendor_file(self):
        """
            Tries to identify OCI provider by reading the file -> /sys/class/dmi/id/chassis_asset_tag # noqa
        """
        self.logger.debug('Checking OCI vendor file')
        oci_path = Path(self.vendor_file)
        if oci_path.is_file():
            if 'OracleCloud' in open(self.vendor_file).read():
                return True
        return False
