from dataclasses import dataclass

import aio_pika
from aio_pika.abc import (
    AbstractChannel,
    AbstractConnection,
    AbstractQueue,
)
from aiormq import AMQPConnectionError

from infrastructure.exceptions.message_broker import MessageBrokerFailedConnectionException
from infrastructure.message_broker.base import BaseMessageBroker
from infrastructure.message_broker.converters import build_message
from infrastructure.message_broker.message import Message


@dataclass
class RabbitMQMessageBroker(BaseMessageBroker):
    connection: AbstractConnection
    channel: AbstractChannel

    async def publish_message(
        self,
        message: Message,
        routing_key: str,
        exchange_name: str,
    ) -> None:
        rq_message: aio_pika.Message = build_message(message)
        await self._publish_message(rq_message, routing_key, exchange_name)

    async def declare_exchange(self, exchange_name: str) -> None:
        await self.channel.declare_exchange(exchange_name, aio_pika.ExchangeType.TOPIC)

    async def _publish_message(
        self,
        rq_message: aio_pika.Message,
        routing_key: str,
        exchange_name: str,
    ) -> None:
        exchange = await self._get_exchange(exchange_name)
        await exchange.publish(rq_message, routing_key=routing_key)

    async def _get_exchange(self, exchange_name: str) -> aio_pika.abc.AbstractExchange:
        return await self.channel.get_exchange(exchange_name, ensure=False)

    async def declare_queue(
        self,
        queue_name: str,
        exchange_name: str,
        routing_key: str,
    ) -> AbstractQueue:
        queue: AbstractQueue = await self.channel.declare_queue(
            queue_name,
            durable=True,
        )
        await queue.bind(exchange_name, routing_key=routing_key)
        return queue

    async def connect(self) -> None:
        try:
            self.connection: AbstractConnection = (
                await self.connection_factory.get_connection()
            )
            self.channel: AbstractChannel = await self.connection.channel()
        except AMQPConnectionError:
            raise MessageBrokerFailedConnectionException()

    async def close(self) -> None:
        await self.connection.close()
