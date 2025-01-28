"""Module for an interactive command-line interface tool instead of basic driver
"""
import os
from pathlib import Path
from json import dump
from typer import Typer, launch
from rich import print
from lib.builder.cletter_builder import CoverLetterBuilder
from lib.builder.tex_writer import TexWriter
from lib.mailer.emailer import Emailer
from lib.db.csv_file_manager import CSVFileManager


CONFIG_PATH = Path(os.getcwd()) / 'config.json'


def check_config_exists(config_path: str) -> None:
    """Checks for the existence of a configuration file; if the file doesn't exist, create the file.

    Args:
        config_path (str): Absolute path to the configuration file.
    """
    if os.path.exists(config_path):
        print(f'Config file exists at {config_path}')
    else:
        print(f'Config file does not exist at {config_path}')

        def generate_default_config(config_path: str) -> None:
            """Generates the expected json config file at the given path.

            Args:
                config_path (str): The path for the config file to be written.
            """
            default_config = {
                "tex": {
                    "stateAgency": "AGENCY",
                    "vacancyID": "00000",
                    "hiringManager": "HIRING MANAGER",
                    "vacancyTitle": "JOB TITLE",
                    "theirStreetNumber": "1 NAME AVE",
                    "theirCityStateZip": "CITY, NY 12345",
                    "theirEmailAddress": "agency@nys.gov"
                },
                "writer": {
                    "texvars_path": "",
                },
                "builder": {
                    "texfile_dir": "",
                    "texfile": "",
                    "output_dir": ".output",
                    "output_filename": "",
                    "builds_dir": ""
                },
                "mailer": {
                    "sender_email": "",
                    "sender_password": "",
                    "smtp_server_address": "smtp.gmail.com",
                    "smtp_port": 587,
                    "attachments": ["", ""]
                },
                "db": {
                    "datafile_path": ""
                }
            }
            with open(config_path, 'w', encoding='utf8') as file:
                dump(default_config, file)
            print(f"Config written to {config_path}")
        generate_default_config(config_path)


app = Typer()

check_config_exists(CONFIG_PATH)


@app.command()
def query_db(vacancy_id: int):
    """Queries the database against a given vacancy ID. Prints vacancy data if successful.

    Args:
        vacancy_id (int): The vacancy ID to be queried against
    """
    manager = CSVFileManager(CONFIG_PATH)
    if manager.record_exists(str(vacancy_id)):
        pass
    else:
        print(f'No records exist for vacancy {str(vacancy_id)}')


@app.command()
def build_send():
    """Generates a cover letter pdf according to the existing state of the latex files.
    The generated pdf can be found in the directory specified in `config.json`
    """
    writer = TexWriter(CONFIG_PATH)
    builder = CoverLetterBuilder(CONFIG_PATH)
    mailer = Emailer(CONFIG_PATH)

    writer.write_tex_string_to_disk()
    builder.generate_pdf_from_tex()
    builder.move_pdf_to_builds(silent=True)

    choice = input('Do you want to send this message? (Y/n): ')
    if choice.lower() == 'y':
        send_email(writer, mailer)


"""
@app.command()
def mangen(show_file=False):
    Generates a cover letter pdf according to a manually defined state.
    
    writer = TexWriter(CONFIG_PATH)
    builder = CoverLetterBuilder(CONFIG_PATH)

    writer.manual_var_input(list(writer.json_vars.keys()))
    writer.write_tex_string_to_disk()

    builder.generate_pdf_from_tex()
    builder.move_pdf_to_builds(silent=True)

    if show_file:
        launch(f"{builder.config['builds_dir']}/{builder.config['output_filename']}.pdf",
               locate=True)

    choice = input('Do you want to send this message? (Y/n): ')
    if choice.lower() == 'y':
        mailer = Emailer(CONFIG_PATH)
        send_email(writer, mailer)
"""


def send_email(writer, mailer):
    """Manually sends the email defined in `config.json`.
    """
    manager = CSVFileManager(CONFIG_PATH)

    # Send email if the vacancyID is not present in the database
    if manager.record_exists(writer.json_vars['vacancyID']):
        print(f"You\'ve already applied to {writer.json_vars['vacancyID']}.")
    else:
        mailer.send_email()
        manager.append_datafile([manager.date, writer.json_vars['vacancyID'],
                                 writer.json_vars['vacancyTitle'].strip(),
                                 writer.json_vars['stateAgency']])


if __name__ == "__main__":
    app()
