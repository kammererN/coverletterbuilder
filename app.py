from pathlib import Path
from builder.cletter_builder import CoverLetterBuilder
from builder.tex_writer import TexWriter
from mailer.emailer import Emailer
import json

CONFIG_PATH_ABS = '/Users/nkam/Documents/code/coverletterbuilder/config.json'

def generate_default_config(config_path: str) -> None:
    default_config = {
        "tex": {
            "stateAgency": "NYS AGENCY",
            "vacancyID": "00000",
            "hiringManager": "HIRING MANAGER",
            "vacancyTitle": "JOB TITLE",
            "theirStreetNumber": "1 NAME AVE",
            "theirCityStateZip": "CITY, NY 12345",
            "theirEmailAddress": "nxrada@gmail.com"
        },
        "writer": {
            "texfile_path": "/Users/nkam/Documents/code/coverletterbuilder/config.json",
            "json_file_path": "/Users/nkam/Documents/code/coverletterbuilder/builder/tex/vars.tex"
        },
        "builder": {
            "tex_file_dir": "tex",
            "main_tex_file": "cletter.tex",
            "output_dir": ".output",
            "output_file_name": "NicholasKammererCoverLetter",
            "builds_dir": "/Users/nkam/Documents/resume-cletter-transcripts"
        },
        "mailer": {
            "sender_email": "nkammerer@alumni.albany.edu",
            "sender_password": "adcb jizg inyy woaq ",
            "smtp_server_address": "smtp.gmail.com",
            "smtp_port": 587,
            "attachments": ["/Users/nkam/Documents/resume-cletter-transcripts/NicholasKammererCoverLetter.pdf", "/Users/nkam/Documents/resume-cletter-transcripts/NicholasKammererResumeJan25.pdf"]
        },
        "db": {
            "data_file_path": ""
        }
    }
    with open(config_path, 'w') as file:
        json.dump(default_config, file)
    print(f"Config written to {config_path}.")


def app():
    writer = TexWriter('/Users/nkam/Documents/code/coverletterbuilder/builder/tex/vars.tex', CONFIG_PATH_ABS)
    builder = CoverLetterBuilder(CONFIG_PATH_ABS)

    # Write TexVars
    writer.compile_tex_string()
    writer.write_tex_string_to_disk()

    # Build Tex PDF
    builder.generate_pdf_from_tex()
    builder.move_pdf_to_builds()

    # Send email
    mailer = Emailer(CONFIG_PATH_ABS)
    mailer.send_email()


if __name__ == "__main__":
    #app()
    generate_default_config(CONFIG_PATH_ABS)