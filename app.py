"""Module for driving the application.
"""

import json
from builder.cletter_builder import CoverLetterBuilder
from builder.tex_writer import TexWriter
from mailer.emailer import Emailer
from db.db import DataFileManager

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
            "texfile_path": "",
        },
        "builder": {
            "tex_file_dir": "tex",
            "main_tex_file": "cletter.tex",
            "output_dir": ".output",
            "output_file_name": "",
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
    print(f"Config written to {config_path}.")


def app() -> None:
    """Main driver for texbuilder, mailer & data manager.
    """
    writer = TexWriter(CONFIG_PATH_ABS)
    builder = CoverLetterBuilder(CONFIG_PATH_ABS)
    mailer = Emailer(CONFIG_PATH_ABS)
    data_mgr = DataFileManager(CONFIG_PATH_ABS)

    # Write TexVars
    writer.write_tex_string_to_disk()

    # Build Tex PDF
    builder.generate_pdf_from_tex()
    builder.move_pdf_to_builds()

    # Send email
    mailer.send_email()
    data_mgr.append_datafile([data_mgr.date, writer.json_vars['vacancyID'],
                              writer.json_vars['vacancyTitle'].strip(),
                              writer.json_vars['stateAgency']])


if __name__ == "__main__":
    app()
