"""Module for handling the writing of texvars from specified json values.
"""
import json


class TexWriter:
    """Class for compiling a tex file from Python-supplied data.
    """

    def __init__(self, config_path_abs: str):
        self.config_path = config_path_abs
        with open(self.config_path, encoding='utf8') as file:
            self.config = json.load(file)['writer']
        with open(self.config_path, encoding='utf8') as file:
            self.json_vars = json.load(file)['tex']
        self.texstring = ""
        self.compile_tex_string(self.json_vars)

    def compile_tex_string(self, input_data: dict, silent=True) -> None:
        """Method for compiling texstring from a dictionary. 
        """
        for key, value in input_data.items():
            self.texstring = self.texstring + \
                f"\\newcommand{{\\{key}}}{{{value}}}\n"
        if not silent:
            print(f"Compiled texstring:\n{self.texstring}")

    def write_tex_string_to_disk(self) -> None:
        """Method for writing self.texstring to disk at object defined texvars path
        """
        print(f"Writing texstring to file {self.config['texvars_path']}")
        with open(self.config['texvars_path'], 'w', encoding='utf8') as file:
            file.write(self.texstring)

    def manual_var_input(self, required_vars: list, silent=True) -> None:
        """Method for manual variable input via cli. 
        Overwrites object's prior texvar config.
        """
        new_var_dict = {}
        for var in required_vars:
            new_var_dict[var] = str(input(f'Input {var}: '))
        print(new_var_dict)
        self.texstring = ""  # Empty texstring
        self.compile_tex_string(new_var_dict)
        self.json_vars = new_var_dict
        if not silent:
            print(f"Compiled texstring:\n{self.texstring}")
