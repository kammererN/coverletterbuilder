"""Module for driving the application.
"""

import json
from lib.builder.cletter_builder import CoverLetterBuilder
from lib.builder.tex_writer import TexWriter
from lib.mailer.emailer import Emailer
from lib.db.csv_file_manager import CSVFileManager

CONFIG_PATH_ABS = '/Users/nkam/Documents/code/coverletterbuilder/config.json'


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
        json.dump(default_config, file)
    print(f"Config written to {config_path}...")


def basic_driver() -> None:
    """Basic driver for texbuilder, mailer & data manager. Basic in the sense
    that it is enitrely ran from within a Python file, and must be ran from
    within a code editor.
    """
    writer = TexWriter(CONFIG_PATH_ABS)
    builder = CoverLetterBuilder(CONFIG_PATH_ABS)
    mailer = Emailer(CONFIG_PATH_ABS)
    data_mgr = CSVFileManager(CONFIG_PATH_ABS)

    # Write TexVars
    writer.write_tex_string_to_disk()

    # Build Tex PDF
    builder.generate_pdf_from_tex()
    builder.move_pdf_to_builds(silent=True)

    # Send email if the vacancyID is not present in the database
    if data_mgr.record_exists(writer.json_vars['vacancyID']):
        print(f'You\'ve already applied to {writer.json_vars['vacancyID']}.')
    else:
        mailer.send_email()
        data_mgr.append_datafile([data_mgr.date, writer.json_vars['vacancyID'],
                                  writer.json_vars['vacancyTitle'].strip(),
                                  writer.json_vars['stateAgency']])


if __name__ == "__main__":
    # generate_default_config(CONFIG_PATH_ABS)
    basic_driver()
