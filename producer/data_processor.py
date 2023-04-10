import os
import sqlite3

import pika
from dotenv import load_dotenv

load_dotenv()

DB_CONNECTION = os.getenv('DB_CONNECTION')


class DbProvider:
    pass


class DbProviderSqlite(DbProvider):

    def __init__(self, db_name, db_tablename):
        self.db_name = db_name
        self.db_tablename = db_tablename
        self.db_connection = sqlite3.connect(self.db_name)

    def init_db(self):
        self.db_connection.execute(
            f"""
                CREATE TABLE IF NOT EXISTS {self.db_tablename} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    event_id INTEGER,
                    status TEXT,
                    match_time TEXT,
                    game_minute INTEGER,
                    game_period INTEGER,
                    home_score INTEGER,
                    away_score INTEGER
                    )
                """
        )

    def write_to_db(self, beat):
        self.db_connection.execute(
            f'INSERT INTO {self.db_tablename} ('
            'event_id, status,'
            'match_time, game_minute,'
            'game_period, home_score,'
            'away_score)'
            'VALUES (?, ?, ?, ?, ?, ?, ?)',
            (
                beat['event_id'], beat['status'],
                beat['match_time'], beat['game_minute'],
                beat['game_period'], beat['home_score'],
                beat['away_score']
            )
        )
        self.db_connection.commit()

    def __del__(self):
        self.db_connection and self.db_connection.close()


class RabbitProvider:
    def __init__(self, rabbitmq_host, queue_name):
        self.rabbitmq_host = rabbitmq_host
        self.queue_name = queue_name
        self.rabbit_connection = None

    def init_rabbit(self):
        self.rabbit_connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=self.rabbitmq_host)
        )
        self.rabbit_channel = self.rabbit_connection.channel()
        self.rabbit_channel.queue_declare(queue=self.queue_name, durable=True)

    def __del__(self):
        self.rabbit_connection and self.rabbit_connection.close()

    def write_to_queue(self, message):
        self.rabbit_channel.basic_publish(
            exchange='',
            routing_key=self.queue_name,
            body=message,
            properties=pika.BasicProperties(delivery_mode=2,)
        )
