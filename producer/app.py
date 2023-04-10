import os

from constant import logs_path
from data_processor import DbProviderSqlite, RabbitProvider
from data_provider import get_provider
from dotenv import load_dotenv

load_dotenv()

DB_NAME = os.getenv('DB_NAME')
DB_TABLENAME = os.getenv('DB_TABLENAME')
RB_HOST = os.getenv('RB_HOST')
QUEUE_NAME = os.getenv('QUEUE_NAME')


def main():
    db = DbProviderSqlite(db_name=DB_NAME, db_tablename=DB_TABLENAME)
    db.init_db()
    rb = RabbitProvider(rabbitmq_host=RB_HOST, queue_name=QUEUE_NAME)
    rb.init_rabbit()
    for message in get_provider().read_game_logs(logs_path):
        db.write_to_db(message.to_dict())
        rb.write_to_queue(message.to_string())


if __name__ == "__main__":
    main()
