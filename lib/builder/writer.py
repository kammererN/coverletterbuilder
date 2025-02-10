"""Module for handling the writing of texvars from specified json values.
"""
import json
from rich.pretty import pprint


class TexWriter:
    """Class for handling the writing of Tex files.
    """

    def __init__(self, config_path_abs: str, texvars_path_abs: str):
        self.config_path = config_path_abs
        self.texvars_path_abs = texvars_path_abs
        with open(self.config_path, encoding='utf8') as file:
            self.config = json.load(file)['writer']
        with open(self.texvars_path_abs, encoding='utf8') as file:
            self.json_vars = json.load(file)
        self.texstring = ""
        self.compile_tex_string(self.json_vars)

    def compile_tex_string(self, input_data: dict, silent=True) -> None:
        """Method for compiling texstring from a dictionary. 
        """
        for key, value in input_data.items():
            self.texstring = self.texstring + \
                f"\\newcommand{{\\{key}}}{{{value}}}\n"
        if not silent:
            pprint(f"Compiled texstring:\n{self.texstring}")

    def write_tex_string_to_disk(self) -> None:
        """Method for writing self.texstring to disk at object defined texvars path
        """
        pprint(f"Writing texstring to file {self.config['texvars_path']}")
        with open(self.config['texvars_path'], 'w', encoding='utf8') as file:
            file.write(self.texstring)

    # TODO: Refactor using rich.prompt
    def manual_var_input(self, required_vars: list, silent=True) -> None:
        """Method for manual variable input via cli. 
        Overwrites object's prior texvar config.
        """
        new_var_dict = {}
        for var in required_vars:
            new_var_dict[var] = str(input(f'Input {var}: '))
        # Add required space after vacanctTitle for tex compilation bug
        new_var_dict['vacancyTitle'] = str(new_var_dict['vacancyTitle']) + " "
        pprint(new_var_dict, expand_all=True)

        self.texstring = ""  # Empty texstring
        self.compile_tex_string(new_var_dict)

        self.write_tex_string_to_disk()

        with open(self.texvars_path_abs, 'w', encoding='utf8') as file:
            json.dump(new_var_dict, file)

        self.json_vars = {}
        self.json_vars = new_var_dict

        if not silent:
            pprint(f"Compiled texstring:\n{self.texstring}")
