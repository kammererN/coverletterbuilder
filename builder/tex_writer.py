"""Module for handling the writing of texvars from specified json values.
"""
import json


class TexWriter:
    """_summary_
    """

    def __init__(self, config_path_abs: str):
        self.config_path = config_path_abs
        with open(self.config_path, encoding='utf8') as file:
            self.config = json.load(file)['writer']
        with open(self.config_path, encoding='utf8') as file:
            self.json_vars = json.load(file)['tex']
        self.texstring = ""
        self.__compile_tex_string()

    def __compile_tex_string(self) -> None:
        """_summary_
        """
        for key, value in self.json_vars.items():
            self.texstring = self.texstring + f"\\newcommand{{\\{key}}}{{{value}}}\n"
        print(f"Compiled texstring:\n{self.texstring}")

    def write_tex_string_to_disk(self) -> None:
        """_summary_
        """
        print(f"Writing texstring to file {self.config['texvars_path']}")
        with open(self.config['texvars_path'], 'w', encoding='utf8') as file:
            file.write(self.texstring)
