import json
from time import sleep
from threading import Thread
from queue import Queue, Empty

import pika
from django.core.mail import send_mail

from app.logging import log


class EmailerThread(Thread):
    def __init__(self, name=None):
        super().__init__(name=name)
        self._connection = None
        self._channel = None
        self._queue = Queue()

    @property
    def _is_connected(self):
        return self._channel and self._channel.is_open

    def _connect(self):
        while True:
            try:
                parameters = pika.URLParameters('amqp://guest:guest@raigfp.2tapp.cc:5672/')
                self._connection = pika.BlockingConnection(parameters)
                self._channel = self._connection.channel()
                return
            except pika.exceptions.AMQPConnectionError:
                log.error('EmailerThread: Failed to to connect to emailer`s message broker.')
                sleep(10)

    def _process_message_queue(self):
        while True:
            connect_close = self._connection.is_closed
            connect_open = self._connection.is_open
            channel_close = self._channel.is_closed
            channel_open = self._channel.is_open
            print("connection is_closed ", connect_close)
            print("connection is_open ", connect_open)
            print("channel is_closed ", channel_close)
            print("channel is_open ", channel_open)
            print("")
            sleep(5)


        while True:
            try:
                message = self._queue.get()

                if not self._is_connected:
                    self._connect()

                self._channel.basic_publish(
                    exchange='',
                    routing_key='email',
                    body=json.dumps(message)
                )

                print(" [x] Sent 'Hello World!'")
            except Exception as error:
                log.error(f'EmailerThread: Failed to send email message. Original error: {error}')
                self._queue.put(message)

    def run(self):
        self._connect()
        self._process_message_queue()

    def send_messages(self, messages):
        # map(self._queue.put, messages)
        for message in messages:
            self._queue.put(message)

    def send_message(self, to, title, body):
        self.send_messages([{'to': to, 'title': title, 'body': body}])


emailer = EmailerThread('EmailerThread')
emailer.start()
