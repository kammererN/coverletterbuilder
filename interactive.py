"""Module for an interactive command-line interface tool instead of basic driver
"""
import os
import sys
from pathlib import Path
from json import dump
from typer import Typer, launch
from rich import print
from rich.prompt import IntPrompt
import inquirer
from lib.builder.builder import CoverLetterBuilder
from lib.builder.writer import TexWriter
from lib.mailer.emailer import Emailer
from lib.db.csv_mgr import CSVFileManager

CONFIG_PATH: Path = Path(os.getcwd()) / 'config.json'
TEXVARS_PATH: Path = Path(os.getcwd()) / 'texvars.json'


def check_config_exists(config_path: str) -> None:
    """Checks for the existence of a config file; if not, create the file.

    Args:
        config_path (str): Absolute path to the configuration file.
    """
    if os.path.exists(path=config_path):
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
            with open(file=config_path, mode='w', encoding='utf8') as file:
                dump(obj=default_config, fp=file)
            print(f"Config written to {config_path}")

        generate_default_config(config_path=config_path)


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
                dump(default_texvars, file)
            print(f"Texvars written to {texvars_path}")

        generate_default_texvars(texvars_path)


app = Typer()

check_config_exists(str(CONFIG_PATH))
check_texvars_exists(str(TEXVARS_PATH))


def send_email():
    """Manually sends the email defined in `config.json`.
    """
    manager = CSVFileManager(str(CONFIG_PATH))
    mailer = Emailer(str(CONFIG_PATH), str(TEXVARS_PATH))
    writer = TexWriter(str(CONFIG_PATH), str(TEXVARS_PATH))

    # Send email if the vacancyID is not present in the database
    if manager.record_exists(writer.json_vars['vacancyID']):
        print(f"You\'ve already applied to {writer.json_vars['vacancyID']}.")
    else:
        mailer.send_email()
        manager.append_datafile((manager.date, writer.json_vars['vacancyID'],
                                 writer.json_vars['vacancyTitle'].strip(),
                                 writer.json_vars['stateAgency']))


def query_db(vacancy_id: int):
    """Queries the database against a given vacancy ID. Prints vacancy data if successful.

    Args:
        vacancy_id (int): The vacancy ID to be queried against
    """
    manager = CSVFileManager(str(CONFIG_PATH))
    if manager.record_exists(str(vacancy_id)):
        pass
    else:
        print(f'No records exist for vacancy {str(vacancy_id)}')


def generate():
    """Generates a cover letter in the form of a .pdf file, using the data in texvars.json
    """
    writer = TexWriter(str(CONFIG_PATH), str(TEXVARS_PATH))
    builder = CoverLetterBuilder(str(CONFIG_PATH))

    writer.write_tex_string_to_disk()
    builder.generate_pdf_from_tex()
    builder.move_pdf_to_builds(silent=True)


def edit():
    """Edits the texvars.json configuration file
    """
    writer = TexWriter(str(CONFIG_PATH), str(TEXVARS_PATH))
    writer.manual_var_input(list(writer.json_vars.keys()))


@app.command()
def interactive():
    """Allows for execution of this program in an interactive manner.
    """
    def clear():
        if os.name == 'nt':
            os.system('cls')
            return
        os.system('clear')

    def hang():
        input("Press any button to continue...")

    try:
        escaped = False
        while not escaped:
            clear()
            questions = [
                inquirer.List(name='choice',
                              message="Select an option to continue",
                              choices=["Query database", "Edit texvars.json",
                                       "Generate cover letter",
                                       "Send email", "Exit"],
                              carousel=True,
                              ),
            ]
            answers = inquirer.prompt(questions)
            clear()
            if "Exit" in answers['choice']:
                escaped = True

            # TODO: Make another case, print database that prints entire DB
            match answers['choice']:
                case 'Query database':
                    # TODO: Make this handle gracefully if the input fails
                    query_db(vacancy_id=int(
                        IntPrompt.ask("Enter the vacancy ID: ")))
                case 'Edit texvars.json':
                    clear()
                    edit()
                case 'Generate cover letter':
                    generate()
                case 'Send email':
                    send_email()
#                case 'View cover letter':
#                    try:
#                        view()
#                    except FileNotFoundError as e:
#                        print(f"Error: {e}")
                case 'Exit':
                    sys.exit(0)
                case __:
                    pass
            hang()

    except KeyboardInterrupt:
        print('Escape detected: closing program.')

    except SystemExit:
        print('System exist deteched: closing program')
        sys.exit(0)


def view():
    """Opens the most recently generated cover letter .pdf in the OS-defined launcher.
    """
    builder = CoverLetterBuilder(str(CONFIG_PATH))
    pdf_path = Path(builder.config['builds_dir']) / \
        builder.config['output_filename']
    pdf_path = f"{pdf_path}.pdf"
    launch(pdf_path)


if __name__ == "__main__":
    app()
