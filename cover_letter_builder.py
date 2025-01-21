# Python script for building a pdflatex cover letter
import subprocess
import json
from pathlib import Path

class CoverLetterBuilder:

    def __init__(self):
        self.runtime_dir = Path(__file__).parent
        self.config_file_path = self.runtime_dir / 'config.json'
        with open(self.config_file_path) as json_file:
            self.config = json.load(json_file)
        self.texfile_dir = self.runtime_dir / self.config['tex_file_dir']
        self.texfile = self.texfile_dir / self.config['main_tex_file']
        self.output_dir = self.runtime_dir / self.config['output_dir']
        self.output_filename = self.config['output_file_name']
        self.pdflatex_command = ['pdflatex', f'-output-directory={self.output_dir}', 
                                 f'-jobname={self.output_filename}', f'{self.texfile}']
        self.builds_dir = self.runtime_dir / self.config['builds_dir']
        self.absolute_download = self.config['abs_down']

    def generate_pdf_from_tex(self) -> None:
        print(f"Generating pdf {self.output_filename} from texfile {self.texfile}")
        subprocess.run(self.pdflatex_command, cwd=self.texfile_dir, stdout=subprocess.DEVNULL)
    
    def move_pdf_to_builds(self) -> None:
        mv_cmd = ['mv', f'{Path(self.output_dir / self.output_filename)}.pdf', f'{Path(self.builds_dir)}']
        subprocess.run(mv_cmd)
        print(f"File {self.output_filename} moved to {self.builds_dir}.")

    def move_pdf_to_downloads(self) -> None:
        mv_cmd = ['mv', f'{Path(self.output_dir / self.output_filename)}.pdf', f'{Path(self.absolute_download)}']
        subprocess.run(mv_cmd)
        print(f"File {self.output_filename} moved to {self.absolute_download}.g")


if __name__ == '__main__':
    print("Run `app.py` instead.")