"""Module for an interactive command-line interface tool instead of basic driver
"""
import os
from pathlib import Path
from json import dump
from typer import Typer, launch
from rich import print
import inquirer
from lib.builder.builder import CoverLetterBuilder
from lib.builder.writer import TexWriter
from lib.mailer.emailer import Emailer
from lib.db.csv_file_manager import CSVFileManager

CONFIG_PATH = Path(os.getcwd()) / 'config.json'
TEXVARS_PATH = Path(os.getcwd()) / 'texvars.json'


def check_config_exists(config_path: str) -> None:
    """Checks for the existence of a config file; if not, create the file.

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


def check_texvars_exists(texvars_path: str) -> None:
    """Checks for the existence of texvar file; if not, create the file.

    Args:
        texvars_path (str): Absolute path to the texvar file.
    """
    if os.path.exists(texvars_path):
        print(f"Config file exists at {texvars_path}")
    else:
        print(f"Config file does not exist at {texvars_path}")

        def generate_default_texvars(texvars_path: str) -> None:
            default_texvars = {
                "stateAgency": "NYS Agency",
                "vacancyID": "000000",
                "hiringManager": "Guy",
                "vacancyTitle": "Job",
                "theirStreetNumber": "1 Name St",
                "theirCityStateZip": "City, ST 123AB",
                "theirEmailAddress": "nxrada@gmail.com"
            }
            with open(texvars_path, encoding='utf8') as file:
                dump(texvars_path, file)
            print(f"Config written to {config_path}")

        generate_default_texvars(texvars_path)


app = Typer()

check_config_exists(CONFIG_PATH)
check_texvars_exists(TEXVARS_PATH)


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
def generate():
    """Generates a cover letter in the form of a .pdf file, using the data in texvars.json
    """
    writer = TexWriter(CONFIG_PATH, TEXVARS_PATH)
    builder = CoverLetterBuilder(CONFIG_PATH)
    mailer = Emailer(CONFIG_PATH, TEXVARS_PATH)

    writer.write_tex_string_to_disk()
    builder.generate_pdf_from_tex()
    builder.move_pdf_to_builds(silent=True)

    choice = input('Do you want to send this message? (Y/n): ')
    if choice.lower() == 'y':
        send_email(writer, mailer)


@app.command()
def interactive():
    menu = [
        inquirer.Checkbox('interests')
    ]


@app.command()
def view():
    """Opens the most recently generated cover letter .pdf in the OS-defined launcher.
    """
    builder = CoverLetterBuilder(CONFIG_PATH)
    pdf_path = builder.config[''] / builder.config['']

    print(f"Opening coverletter {pdf_path}...")
    launch()


if __name__ == "__main__":
    app()
