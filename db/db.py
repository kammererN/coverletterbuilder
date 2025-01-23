
# TODO: Add csv data handler
import csv
import json
import datetime

class DataFileManager:

    def __init__(self, config_path_abs: str):
        # Import config file
        with open(config_path_abs, 'r') as file:
            self.config = json.load(file)['db']
        
        self.date = str(datetime.datetime.now().date())

    def append_datafile(self, data: list) -> None:
        try:
            with open(self.config['datafile_path'], 'a', newline='') as csvfile:
                df_writer = csv.writer(csvfile)
                df_writer.writerow(data)
        except Exception as e:
            print(f"Error when appending datafile: {e}")

    def get_datafile(self) -> list:
        with open(self.config['datafile_path'], 'r', newline='') as csvfile:
            datafile = csv.reader(csvfile, delimiter=',')
            rows = list(datafile)
        return rows

    def print_datafile(self) -> None:
        for row in self.get_datafile():
            print(row)