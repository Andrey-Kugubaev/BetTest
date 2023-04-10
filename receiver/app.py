import os

from data_processor import Receiver
from dotenv import load_dotenv

load_dotenv()

RB_HOST = os.getenv('RB_HOST')
QUEUE_NAME = os.getenv('QUEUE_NAME')


def main():
    receive = Receiver()
    receive.start_consuming()


if __name__ == "__main__":
    main()
