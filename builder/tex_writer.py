
import json

class TexWriter:
    def __init__(self, texfile_path: str, json_file_path: str):
        self.texfile_path = texfile_path
        self.json_file_path = json_file_path
        self.json_vars = self.__read_tex_config()
        self.texstring = ""

    def __read_tex_config(self) -> dict:
        with open(self.json_file_path) as file:
            texdata = json.load(file)

        return texdata["tex"]
    
    def compile_tex_string(self) -> None:
        for key, value in self.json_vars.items():
            self.texstring = self.texstring + f"\\newcommand{{\\{key}}}{{{value}}}\n"
        
        print(f"Compiled texstring:\n{self.texstring}")
        
    def write_tex_string_to_disk(self) -> None:
        print(f"Writing texstring to file {self.texfile_path}")
        with open(self.texfile_path, 'w') as file:
            file.write(self.texstring)
