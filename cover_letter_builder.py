# Python script for building a pdflatex cover letter
import subprocess
import json
from pathlib import Path
from pdflatex import PDFLaTeX


class CoverLetterBuilder:

    def __init__(self):
        self.runtime_dir = Path(__file__).parent
        self.config_file_path = self.runtime_dir / 'config.json'
        with open(self.config_file_path) as json_file:
            self.config = json.load(json_file)
        self.tex_file_dir = self.runtime_dir / self.config['tex_file_dir']
        self.main_tex_file = self.tex_file_dir / self.config['main_tex_file']
        self.output_dir = self.runtime_dir / self.config['output_dir']
        self.output_filename = self.config['output_file_name']
        self.pdflatex_command = ['pdflatex', f'-output-directory={self.output_dir}', 
                                 f'-jobname={self.output_filename}', f'{self.main_tex_file}']
        self.builds_dir = self.runtime_dir / self.config['builds_dir']

    def generate_pdf_from_tex(self) -> None:
        subprocess.run(self.pdflatex_command)
        self.move_pdf_to_builds()
    
    def move_pdf_to_builds(self) -> None:
        subprocess.run(['mv', f'{Path(self.output_dir / self.output_filename)}.pdf', f'{Path(self.builds_dir)}'])

    def generate_using_python_api(self):
        pdflatex_api = PDFLaTeX.from_texfile(f'{self.main_tex_file}')
        pdf, log, completed_process = pdflatex_api.create_pdf(keep_pdf_file=False, keep_log_file=False)
        return pdf

if __name__ == '__main__':
    builder = CoverLetterBuilder()
    print(builder.pdflatex_command)
    #builder.generate_pdf_from_tex()
    pdf = builder.generate_using_python_api()
    print(pdf)