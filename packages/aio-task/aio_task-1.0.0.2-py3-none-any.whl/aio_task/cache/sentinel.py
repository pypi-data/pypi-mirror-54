""" Cache implementation based on aioredis for a redis sentinel storage.

:warning: This API has not yet stabilized and may change in future releases.
"""
import asyncio
import logging

import aioredis

from aio_task.task import Task
from aio_task.cache import CacheABC


async def acquire_connection_pool(sentinels):
    """ Get connection pool to sentinel.

    :param list(tuple) sentinels: sentinels to connect to
    :returns: SentinelPool
    """
    logging.debug(f"Create sentinel pool: {sentinels}")
    try:
        return await aioredis.sentinel.pool.create_sentinel_pool(sentinels)
    except Exception as exc:
        if "Could not connect" not in str(exc):
            raise exc
    logging.warning("Fail to connect. Try again in a second...")
    await asyncio.sleep(1)
    return await acquire_connection_pool(sentinels)


class Cache(CacheABC):
    """ Cache implementation. """

    def __init__(self, ttl, mastername, cache_conf):
        self.ttl = ttl
        self.mastername = mastername
        self._cache_conf = cache_conf
        self.pool = None

    @classmethod
    async def create(cls, cache_conf):
        """ Create a new cache instance.

        :param dict cache_conf: params for
            aioredis.sentinel.create_sentinel_pool + ttl + name
        :rtype: Cache
        """
        logging.info("create sentinel cache.")
        try:
            ttl = cache_conf.pop("ttl")
        except KeyError:
            ttl = cls.TTL
        try:
            mastername = cache_conf.pop("mastername")
        except KeyError:
            mastername = "mymaster"
        cache = cls(ttl, mastername, cache_conf)
        logging.info(f"ttl: {ttl}, mastername: {mastername}")
        await cache.connect()
        await cache.sentinel.ping()
        await cache.redis.ping()
        return cache

    @property
    def sentinel(self):
        """ Get a sentinel from the sentinel's pool. """
        return aioredis.sentinel.RedisSentinel(self.pool)

    @property
    def redis(self):
        """ Get :class:`~.Redis` client to named master.
        The client is instantiated with special connections pool which
        is controlled by :class:`SentinelPool`.

        :rtype: aioredis.Redis
        """
        return self.sentinel.master_for(self.mastername)

    async def connect(self):
        """ Acquire a connection to redis pool. """
        logging.info("connect to sentiel.")
        self.pool = await acquire_connection_pool(**self._cache_conf)
        await self.pool.discover(timeout=1)

    async def close(self):
        """ Shutdown the cache. """
        logging.info("close sentiel cache.")
        if self.pool is not None:
            self.pool.close()
            await self.pool.wait_closed()

    async def save_task(self, task, ttl=None):
        """ Store a task.

        :param int ttl: Time to keep task in cache, default TTL
        :param aio_task.task.Task task:
        """
        logging.debug("save task")
        await self.redis.set(task.task_id, task.dump(), expire=ttl or self.ttl)

    async def get_task(self, task_id):
        """ Get a task from its id.

        :param str task_id:
        :rtype: aio_task.task.Task
        :raises: ValueError if task not found
        """
        logging.debug("get task")
        data = await self.redis.get(task_id)
        if data is None:
            raise ValueError(task_id)

        return Task.load(data.decode())
