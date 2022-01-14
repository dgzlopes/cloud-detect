import asyncio
import logging
import time
from sys import version_info as py_version

from cloud_detect.providers import AlibabaProvider
from cloud_detect.providers import AWSProvider
from cloud_detect.providers import AzureProvider
from cloud_detect.providers import DOProvider
from cloud_detect.providers import GCPProvider
from cloud_detect.providers import OCIProvider

__PROVIDER_CLASSES = [
    AlibabaProvider, AWSProvider, AzureProvider,
    DOProvider, GCPProvider, OCIProvider,
]


async def _identify(timeout):

    assert timeout is None or (isinstance(timeout, (int, float)) and timeout > 0.1), \
        f'`timeout` should be a number and > 0.1, provided value: {timeout}'

    async def wrapper(prov):
        try:
            return await prov().identify()
        except asyncio.CancelledError:
            pass

    tasks = {
        prov.identifier: asyncio.ensure_future(wrapper(prov)) for prov in __PROVIDER_CLASSES
    }

    async def cancel_unfinished_tasks():
        for t in tasks.values():
            if not t.done():
                t.cancel()
        # This statement ensures
        # "Task was destroyed but it is pending!" warning is not raised
        await asyncio.gather(*tasks.values())

    if timeout is None:
        def time_ok(): return True
    else:
        stoptime = time.time() + timeout
        def time_ok(): return time.time() < stoptime

    while tasks and time_ok():
        for prov in list(tasks):
            t = tasks[prov]
            if t.done():
                del tasks[prov]
                if t.result():
                    await cancel_unfinished_tasks()
                    logging.debug(f'Cloud_detect result is {prov}')
                    return prov
        else:
            await asyncio.sleep(0.1)
            continue

    if tasks:
        await cancel_unfinished_tasks()

    return 'unknown'


def provider(timeout=None):
    """
        Identify the host's cloud provider

        :param: timeout(optional) Maximum time(seconds) allowed for detection.
            On timeout, 'unknown' is returned.
            When the host is one of the SUPPORTED_PROVIDERS,
            the correct cloud provider is deteced, usually, within a second or two.
            When the host is your local or a non-supported provider,
            it may take more than a minute to return 'unknown'.
            Such a long wait time may not be desirable in certain use cases and
            `timeout` can be used to reduce it.
        :return: :str: 'unknown' or one of the SUPPORTED_PROVIDERS

        If you want the async counterpart of this function, use `async_provider`.

        Usage::
        >>> from cloud_detect import provider, SUPPORTED_PROVIDERS
        >>> SUPPORTED_PROVIDERS
        ('aws', 'azure', 'gcp')
        >>> provider()
        'aws'
    """
    if py_version.minor >= 7:
        result = asyncio.run(_identify(timeout))
    else:
        loop = asyncio.new_event_loop()
        result = loop.run_until_complete(_identify(timeout))
        loop.close()
    return result


async def async_provider(timeout=None):
    """
        The async counterpart of `provider`.
        Use this api when calling from async code.
        Usage::
        >>> from cloud_detect import async_provider
        >>> async def my_async_func():
                ....
                cloud = await async_provider()
                ....
    """
    return await _identify(timeout)


SUPPORTED_PROVIDERS = tuple(sorted(p.identifier for p in __PROVIDER_CLASSES))
