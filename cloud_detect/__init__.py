import asyncio
import logging
import time
from sys import version_info

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

TIMEOUT = 5  # seconds


async def _identify(timeout):
    tasks = {
        prov.identifier: asyncio.ensure_future(
            prov().identify(),
        ) for prov in __PROVIDER_CLASSES
    }

    async def cancel_unfinished_tasks():
        for t in tasks.values():
            if not t.done():
                try:
                    t.cancel()
                except asyncio.CancelledError:
                    pass
        # This statement ensures
        # "Task was destroyed but it is pending!" warning is not raised
        await asyncio.gather(*tasks.values())

    stoptime = time.time() + timeout
    while tasks and time.time() < stoptime:
        for prov in list(tasks):
            t = tasks[prov]
            if t.done():
                del tasks[prov]
                if t.result():
                    await cancel_unfinished_tasks()
                    logging.debug('Cloud_detect result is %s' % prov)
                    return prov
        else:
            await asyncio.sleep(0.1)
            continue

    if tasks:
        await cancel_unfinished_tasks()
        return 'timeout'
    else:
        return 'unknown'


def provider(timeout=TIMEOUT):
    if version_info.minor >= 7:
        result = asyncio.run(_identify(timeout))
    else:
        loop = asyncio.new_event_loop()
        result = loop.run_until_complete(_identify(timeout))
        loop.close()
    return result


async def async_provider(timeout=TIMEOUT):
    return await _identify(timeout)


SUPPORTED_PROVIDERS = tuple(sorted(p.identifier for p in __PROVIDER_CLASSES))
