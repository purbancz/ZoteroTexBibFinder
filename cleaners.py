import regex


class DummyLinesCleaner:
    @staticmethod
    def clean_dummy_lines(tex_lines):
        new_tex_lines = []
        for line in tex_lines:
            line = line.strip().replace(" +", " ")
            left_bracket = line.count('{')
            right_bracket = line.count('}')
            if (line.startswith("\\documentclass") or line.startswith("\\usepackage") or line.startswith("\\newcommand")
                    or line.startswith("\\renewcommand") or line.startswith("\\setlength") or line.startswith(
                        "\\hypersetup")
                    or line.startswith("\\makeatletter") or line.startswith("\\makeatother")
                    or line.startswith("%") or line.startswith("\\providecommand") or line.startswith("\\liststyle")
                    or line.startswith("\\pagestyle")
            ):
                continue
            if line.startswith("{") and left_bracket > right_bracket:
                continue
            if left_bracket < right_bracket and line.endswith("}"):
                line = line[:-1]
            new_tex_lines.append(line + "\n")
            if line.startswith("\\sub"):
                new_tex_lines.append("")
        return new_tex_lines


class DummyCharactersCleaner:
    @staticmethod
    def clear_dummy_characters(tex_lines):
        for i in range(len(tex_lines)):
            s = regex.sub(" +", " ", tex_lines[i].strip())
            s = s.replace("\\ ", "")
            s = s.replace("„", ",,")
            s = s.replace("”", "''")
            s = s.replace("’", "'")
            s = s.replace("“", "``")
            s = s.replace(" s. ", " s.~")
            s = s.replace(" ss. ", " ss.~")
            s = s.replace(" t. ", " t.~")
            s = s.replace(" rozdz. ", " rozdz.~")
            s = s.replace(" r. ", "~r.")
            s = s.replace(" – ", " -- ")
            s = s.replace("—", "---")
            s = s.replace("\\par", "")
            s = regex.sub(" +", " ", s.strip())
            s = regex.sub("(\\s)([a-zA-Z])\\s", "\\1\\2~", s)
            s = regex.sub("(\\{)([a-zA-Z])\\s", "\\1\\2~", s)
            s = regex.sub("^([a-zA-Z])\\s", "\\1~", s)
            s = regex.sub("\\\\[a-zA-Z]{1,}\\{\\s?\\}", "", s)
            s = regex.sub("(\\\\[sub]{0,}section)(\\[.{1,}\\])?\\{(\\s?\\d\\.\\s)?(.{1,})\\}", "\\1\\{\\4\\}", s)
            s = regex.sub("(\\s)([\\.,?!;]{1}|'')(\\s)", "\\2\\3", s)
            s = regex.sub("(,,)(\\s)", "\\1", s)

            s = DummyCharactersCleaner.clear_left_bracket("textit", s)
            s = DummyCharactersCleaner.clear_right_bracket("textit", s)
            s = DummyCharactersCleaner.clear_left_bracket("textbf", s)
            s = DummyCharactersCleaner.clear_right_bracket("textbf", s)
            s = regex.sub(" +", " ", s.strip())
            s = s.replace("\\textbf{ }", " ")
            s = s.replace("\\textit{ }", " ")
            s = s.replace("\\textbf{}", "")
            s = s.replace("\\textit{}", "")
            s = s.replace("\\footnote{ ", "\\footnote{")

            s = regex.sub(r"(\\(?:sub)*section\{)(.*?)\\(\})", r"\1\2}",
                          regex.sub(r"(\\(?:sub)*section)\\(\{)", r"\1\2", s))
            s = regex.sub(r"(\\(?:sub)*section\{)(?:\d+(?:\.\d+)*\.?\s*)?(.*?)\}", r"\1\2}", s)

            tex_lines[i] = s

    @staticmethod
    def clear_left_bracket(enviroment, text):
        regex_pattern = "(\\\\" + enviroment + "\\{)([^\\p{L}\\\\])"
        while regex.search(regex_pattern, text):
            text = regex.sub(regex_pattern, "\\2\\1", text, count=1)
        return text

    @staticmethod
    def clear_right_bracket(enviroment, text):
        regex_pattern = "(\\\\" + enviroment + "\\{.{0,}?)([^\\p{L}0-9\\.])(\\})"
        return regex.sub(regex_pattern, "\\1\\3\\2", text, count=1)


class BibFileCleaner:
    fields_to_remove = [
        'month =',
        'file =',
        'abstract =',
        'copyright =',
        'language =',
        'isbn =',
        'issn =',
        'keywords =',
    ]

    def __init__(self):
        self.cleaned_content = []

    def clean_bib_content(self, bib_content):
        for line in bib_content:
            if not any(field in line for field in self.fields_to_remove):
                self.cleaned_content.append(line)
        return self.cleaned_content

    @staticmethod
    def read_bib_file(file_path):
        with open(file_path, 'r') as file:
            return file.readlines()

    @staticmethod
    def write_bib_file(file_path, cleaned_content):
        with open(file_path, 'w') as file:
            file.writelines(cleaned_content)

# Example usage:
# file_path = 'path_to_your.bib'
# bib_content = BibFileCleaner.read_bib_file(file_path)

# cleaner = BibFileCleaner(bib_content)
# cleaned_content = cleaner.clean_bib_content()

# BibFileCleaner.write_bib_file(file_path, cleaned_content)
