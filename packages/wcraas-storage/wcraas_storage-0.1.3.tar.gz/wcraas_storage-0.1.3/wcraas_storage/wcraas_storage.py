# -*- coding: utf-8 -*-

"""The WCraaS Storage module is responsible for providing storage services for the platform."""

import asyncio
import json
import logging
import aio_pika

from aio_pika import connect_robust, IncomingMessage, ExchangeType
from aio_pika.patterns import RPC
from aio_pika.pool import Pool
from typing import Dict
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from wcraas_common import AMQPConfig, WcraasWorker
from wcraas_common.decorator import is_rpc, consume
from wcraas_storage.config import MongoConfig


class StorageWorker(WcraasWorker):
    def __init__(
        self,
        amqp: AMQPConfig,
        mongo: MongoConfig,
        mapping: Dict[str, str],
        loglevel: int,
        *args,
        **kwargs,
    ):
        super().__init__(amqp, loglevel)
        self.mongo = mongo
        self.logger = logging.getLogger("wcraas.storage")
        self.logger.setLevel(loglevel)
        self._db = AsyncIOMotorClient(mongo.host, mongo.port)[mongo.db]
        self._close = asyncio.Event()
        self.mapping = mapping

    def _discover_callable(self, *args, **kwargs):
        """
        Overwride common module's callable check to exclude AsyncIOMotorDatabase.

        AsyncIOMotorDatabase instances return (and create) a new collection refference
        when their `__getattr__` is invoked and will thus always pass `_discover`.
        """
        for attr in super()._discover_callable(*args, **kwargs):
            if isinstance(attr, AsyncIOMotorDatabase):
                continue
            yield attr

    def get_queue_by_collection(self, collection):
        """
        Return the queue that corresponds to the given collection.

        :param collection: The collection with which to determine the queue.
        :type collection: string
        """
        for k, v in self.mapping.items():
            if v == collection:
                return k
        raise KeyError

    async def store(self, message: IncomingMessage) -> None:
        """
        AMQP consumer function, that inserts an `IncomingMessage`'s json-loaded body in a MongoDB collection based on the source exchange.

        :param message: The message that trigered the consume callback.
        :type message: aio_pika.IncomingMessage
        """
        async with message.process():
            try:
                result = await self._db[self.mapping[message.exchange]].insert_one(
                    json.loads(message.body)
                )
                self.logger.info(result)
            except Exception as err:
                self.logger.error(err)

    @is_rpc("list_collections")
    async def list_collections(self):
        """
        AMQP function that lists available collections in selected MongoDB.
        """
        return {
            "data": [
                {
                    "name": collection["name"],
                    "type": collection["type"],
                    "queue": self.get_queue_by_collection(collection["name"]),
                    "count": await self._db[collection["name"]].estimated_document_count(),
                }
                for collection in (await self._db.list_collections())
            ]
        }

    async def start(self) -> None:
        """
        Asynchronous runtime for the worker, responsible of managing and maintaining async context open.
        """
        async with self._amqp_pool.acquire() as sub_channel:
            await sub_channel.set_qos(prefetch_count=1)
            # Not using the common module's `start_consume` because the consumer function is the same for
            # multiple consume queues and dynamically creating new function names in the class in order to
            # decorate them (which would enable using `start_consume`) would be too much of a hack.
            for queue_name, collection in self.mapping.items():
                await self.register_consumer(sub_channel, self.store, queue_name)
                self.logger.warning(f"Registered {queue_name} ...")
            await self.start_rpc()

    def run(self) -> None:
        """
        Helper function implementing the synchronous boilerplate for initilization and teardown.
        """
        loop = asyncio.get_event_loop()
        try:
            loop.run_until_complete(self.start())
        except KeyboardInterrupt:
            self.logger.info("[x] Received ^C ! Exiting ...")
        finally:
            self._close.set()
            loop.shutdown_asyncgens()
