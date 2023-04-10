import json
import os

from message import JsonMessage


class DataProvider:
    pass


class DataProviderLocalJson(DataProvider):

    def __init__(self):
        super().__init__()

    def read_game_logs(self, folder_path):
        for file_logs in os.listdir(folder_path):
            if file_logs.endswith('logs.json'):
                logs_path = os.path.join(folder_path, file_logs)
                with open(logs_path) as f:
                    json_data = json.load(f)

                for elem in json_data:
                    yield JsonMessage(elem)


def get_provider():
    return DataProviderLocalJson()
