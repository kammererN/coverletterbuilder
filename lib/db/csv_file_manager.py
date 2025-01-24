"""Module for managing the logging of app data to CSV.
"""
import csv
import json
import datetime


class CSVFileManager:
    """Class for managing basic CRUD activities using a CSV datafile.
    """

    def __init__(self, config_path_abs: str):
        # Import config file
        with open(config_path_abs, 'r', encoding='utf8') as file:
            self.config = json.load(file)['db']

        self.date = str(datetime.datetime.now().date())

    def append_datafile(self, data: list) -> None:
        """Appends a given list to the csvfile specified in self.config[]

        Args:
            data (list): A list of data to be appended to the datafile.
        """
        with open(self.config['datafile_path'], 'a', newline='', encoding='utf8') as csvfile:
            df_writer = csv.writer(csvfile)
            df_writer.writerow(data)

    def get_datafile(self) -> list:
        """Retrieves the csv csvfile specified at self.config[]

        Returns:
            list: A list representation of the csv file
        """
        with open(self.config['datafile_path'], 'r', newline='', encoding='utf8') as csvfile:
            datafile = csv.reader(csvfile, delimiter=',')
            rows = list(datafile)
        return rows

    def print_datafile_by_row(self) -> None:
        """Prints the datafile by row.
        """
        for row in self.get_datafile():
            print(row)

    def record_exists(self, record: str) -> bool:
        """Recurses through the csvfile and returns true if the record is present

        Args:
            record (str): A string to search the database for

        Returns:
            bool: A boolean representation of the record's existence
        """
        try:
            with open(self.config['datafile_path'], 'r', encoding='utf8') as file:
                reader = csv.reader(file)

                # Process each row recursively
                def process_row(row):
                    for cell in row:
                        if record in cell:
                            print(f'{row}')
                            return True
                    return False

                # Start from the first row
                current_row = next(reader)
                while current_row:
                    if process_row(current_row):
                        return True
                    current_row = next(reader, None)

            return False

        except FileNotFoundError:
            print(f"Error: File '{self.config['datafile_path']}' not found.")
            return False
        except Exception as e:
            print(f"An error occurred: {e}")
            return False
