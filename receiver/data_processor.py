import json
import os

import pika
from dotenv import load_dotenv
from match_logger import MatchLogger
from memory import Memo
from validator import is_valid

load_dotenv()

RB_HOST = os.getenv('RB_HOST')
QUEUE_NAME = os.getenv('QUEUE_NAME')


class STATUSES():
    GAME_END = "game_end"


class Receiver(object):
    def __init__(self, stop_on_status=STATUSES.GAME_END):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=RB_HOST)
        )
        self.channel = self.connection.channel()
        self.queue_name = QUEUE_NAME
        self.channel.queue_declare(queue=self.queue_name, durable=True)
        self.memo = Memo()
        self.dp = MatchLogger(self.memo)

        self.stop_on_status = stop_on_status

    def cb(self, ch, method, params, body):
        body = json.loads(body)

        if not self.memo.is_ready() or is_valid(self.memo.to_dict(), body):
            self.memo.update(body)
            self.dp.save_result()
            ch.basic_ack(delivery_tag=method.delivery_tag)
        else:
            body["status"] = "failed"
            self.memo.update(body)
            self.dp.save_result()
            self.stop_consuming()

        if (self.stop_on_status and
                self.memo.is_ready() and
                self.memo.to_dict()["status"] == self.stop_on_status):
            self.stop_consuming()

    def start_consuming(self):
        self.channel.basic_consume(
            queue=self.queue_name, on_message_callback=self.cb
        )
        self.channel.start_consuming()

    def stop_consuming(self):
        self.connection.close()

    def __del__(self):
        self.connection and self.connection.close()
