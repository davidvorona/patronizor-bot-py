import os
import json
from config import *

class Storage:
    @staticmethod
    def validate_data_dir(data_dir: str):
        data_dir_exists = os.path.isdir(data_dir)
        if data_dir_exists == False:
            print('Cannot start bot without data directory, aborting')
            raise Exception('No data directory')

    data_dir = DATA_DIR

    def __init__(self, file_name: str, override_path: bool = False):
        self.file_path = file_name if override_path else f'{self.data_dir}/{file_name}'
        file_exists = os.path.isfile(self.file_path)
        if file_exists == False:
            with open(self.file_path, 'x') as file:
                print('File ' + file.name + ' created')

    def read(self):
        try:
            with open(self.file_path, 'r') as file:
                data = json.loads(file.read())
                print(file.name + ' loaded')
                return data
        except FileNotFoundError as err:
            print(err)
            raise
        except json.decoder.JSONDecodeError:
            if os.stat(self.file_path).st_size > 0:
                print('Warning: invalid data in ' + file.name)
            pass

    def write(self, data: list = None):
        if data is not None:
            try:
                with open(self.file_path, 'w') as file:
                    file.write(json.dumps(data))
            except:
                raise

    def add(self, new_str: str = None):
        if new_str is not None:
            data = self.read() or []
            data.append(new_str)
            try:
                with open(self.file_path, 'w') as file:
                    file.write(json.dumps(data))
            except:
                raise

