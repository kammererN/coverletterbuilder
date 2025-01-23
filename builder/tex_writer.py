
import json

class TexWriter:
    
    def __init__(self, config_path_abs: str):
        self.config_path = config_path_abs
        with open(self.config_path) as file:
            self.config = json.load(file)['writer']
        with open(self.config_path) as file:    
            self.json_vars = json.load(file)['tex']
        self.texstring = ""
        self.__compile_tex_string()
    
    def __compile_tex_string(self) -> None:
        for key, value in self.json_vars.items():
            self.texstring = self.texstring + f"\\newcommand{{\\{key}}}{{{value}}}\n"
        print(f"Compiled texstring:\n{self.texstring}")
    
    def write_tex_string_to_disk(self) -> None:
        print(f"Writing texstring to file {self.config['texfile_path']}")
        with open(self.config['texfile_path'], 'w') as file:
            file.write(self.texstring)
