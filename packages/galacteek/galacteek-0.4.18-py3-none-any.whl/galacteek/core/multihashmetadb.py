import asyncio
import aiofiles
import os.path
import os
import json

from galacteek import log
from galacteek.ipfs.cidhelpers import stripIpfs
from galacteek.ipfs.cidhelpers import isIpfsPath


class IPFSObjectMetadataDatabase:
    """
    Basic file-based database to hold metadata about IPFS objects by path
    """

    def __init__(self, metaDbPath, loop=None):
        self._metaDbPath = metaDbPath
        self._lock = asyncio.Lock(
            loop=loop if loop else asyncio.get_event_loop())

    @property
    def metaDbPath(self):
        return self._metaDbPath

    def path(self, rscPath):
        if isinstance(rscPath, str) and isIpfsPath(rscPath):
            path = stripIpfs(
                rscPath.rstrip('/')).replace('/', '_')
            comps = path.split('/')

            if len(comps) > 0:
                containerId = comps[0][0:8]
                containerPath = os.path.join(self.metaDbPath, containerId)
                metaPath = os.path.join(containerPath, path)
                return containerPath, metaPath, os.path.exists(metaPath)

        return None, None, False

    async def write(self, metaPath, metadata, mode='w+t'):
        async with aiofiles.open(metaPath, mode) as fd:
            await fd.write(
                json.dumps(metadata, indent=4)
            )

    async def store(self, rscPath, **data):
        containerPath, metaPath, exists = self.path(rscPath)
        if metaPath and not exists:
            await asyncio.sleep(0)
            with await self._lock:
                if not os.path.isdir(containerPath):
                    os.mkdir(containerPath)
                try:
                    await self.write(metaPath, data)
                except BaseException:
                    log.debug('Error storing metadata for {0}'.format(
                        rscPath))
                else:
                    log.debug('{0}: stored metadata {1}'.format(rscPath, data))
        elif metaPath and exists:
            # Patch the existing metadata
            await asyncio.sleep(0)

            metadata = await self.get(rscPath)
            if not isinstance(metadata, dict):
                return

            with await self._lock:
                for key, value in data.items():
                    if key not in metadata:
                        metadata[key] = value
                try:
                    await self.write(metaPath, metadata)
                except BaseException:
                    pass

    async def get(self, rscPath):
        containerPath, metaPath, exists = self.path(rscPath)
        if metaPath and exists:
            await asyncio.sleep(0)
            with await self._lock:
                try:
                    async with aiofiles.open(metaPath, 'rt') as fd:
                        data = await fd.read()
                        return json.loads(data)
                except BaseException as err:
                    # Error reading metadata
                    log.debug('Error reading metadata for {0}: {1}'.format(
                        rscPath, str(err)))
                    os.unlink(metaPath)
