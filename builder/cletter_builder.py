"""Module for generating a pdf coverletter based on a given texfile.
"""
import subprocess
import json


class CoverLetterBuilder:
    """Class for generating a pdf coverletter based on a given texfile.
    """

    def __init__(self, config_path_abs: str):
        self.config_path_abs = config_path_abs
        with open(self.config_path_abs, encoding='utf8') as json_file:
            self.config = json.load(json_file)['builder']

    def generate_pdf_from_tex(self) -> None:
        """Generates a pdf file according to the given texfile path.
            """
        cmd = {
            'out_dir': f'-output-directory={self.config['output_dir']}',
            'jobname': f'-jobname={self.config['output_filename']}',
            'texfile': f'{self.config['texfile']}',
            'bin': 'pdflatex',
        }
        cmd_list = [cmd['bin'], cmd['out_dir'], cmd['jobname'], cmd['texfile']]
        print(f"Generating pdf {self.config['output_filename']
                                } from texfile {self.config['texfile']}")
        subprocess.run(cmd_list, cwd=self.config['texfile_dir'],
                       stdout=subprocess.DEVNULL, check=False)

    def move_pdf_to_builds(self) -> None:
        """Moves a generated PDF file to the directory specified in
            """
        cmd = {
            'from': f'{self.config['builds_dir']}/{self.config['output_filename']}.pdf',
            'to': f'{self.config['builds_dir']}',
            'bin': 'mv'
        }

        cmd_list = [cmd['bin'], cmd['from'], cmd['to']]

        subprocess.run(cmd_list, check=False)
        print(f"File {cmd['from']} moved to {cmd['to']}.")
