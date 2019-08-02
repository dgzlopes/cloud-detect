from abc import ABCMeta, abstractmethod


class AbstractProvider():
    """
        Abstract class representing a cloud provider.
        All concrete cloud providers should implement this.
    """

    @abstractmethod
    def identify(self):
        pass  # pragma: no cover

    @abstractmethod
    def check_metadata_server(self):
        pass  # pragma: no cover

    @abstractmethod
    def check_vendor_file(self):
        pass  # pragma: no cover
