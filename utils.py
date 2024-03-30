class TexParser:
    @staticmethod
    def parse_tex_file(file_name):
        with open(file_name, 'r', encoding="utf-8") as file:
            tex_lines = file.readlines()
        return tex_lines


class SaveFile:
    @staticmethod
    def rewrite_file(path_to_file, text):
        with open(path_to_file, 'w', encoding="utf-8") as file:
            for line in text:
                file.write(line + '\n')

    @staticmethod
    def rewrite_file_single_par(path_to_file, text):
        with open(path_to_file, 'w', encoding="utf-8") as file:
            file.writelines(text)
