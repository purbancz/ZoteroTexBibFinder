import regex
import unicodedata


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

            s = regex.sub(r"\\textcolor\{[^}]*\}\{([^}]*)\}", r"\1", s)
            s = regex.sub(r"\\textrm\{([^}]*)\}", r"\1", s)
            s = regex.sub(r"\\textstyleDomylnaczcionkaakapitu\{([^}]*)\}", r"\1", s)

            s = regex.sub("(\\s)([a-zA-Z])\\s", "\\1\\2~", s)
            s = regex.sub("(\\{)([a-zA-Z])\\s", "\\1\\2~", s)
            s = regex.sub("^([a-zA-Z])\\s", "\\1~", s)

            s = regex.sub("(\\\\[sub]{0,}section)(\\[.{1,}\\])?\\{(\\s?\\d\\.\\s)?(.{1,})\\}", "\\1{\\4}", s)
            s = regex.sub("(\\s)([\\.,?!;]{1}|'')(\\s)", "\\2\\3", s)
            s = regex.sub("(,,)(\\s)", "\\1", s)

            # c
            s = regex.sub(r"\b(\d+)(st|nd|rd|th)\b", r"\1\\textsuperscript{\2}", s)

            s = regex.sub(" +", " ", s.strip())
            s = s.replace("\\textbf{ }", " ")
            s = s.replace("\\textit{ }", " ")
            s = s.replace("\\textbf{}", "")
            s = s.replace("\\textit{}", "")

            s = DummyCharactersCleaner.clear_left_bracket("textit", s)
            s = DummyCharactersCleaner.clear_right_bracket("textit", s)
            s = DummyCharactersCleaner.clear_left_bracket("textbf", s)
            s = DummyCharactersCleaner.clear_right_bracket("textbf", s)

            s = regex.sub("\\\\[a-zA-Z]{1,}\\{\\s?\\}", "", s)

            s = s.replace("\\footnote{ ", "\\footnote{")

            # s = regex.sub(r"(\\(?:sub)*section\{)(.*?)\\(\})", r"\1\2}",
            #               regex.sub(r"(\\(?:sub)*section)\\(\{)", r"\1\2", s))
            s = regex.sub(r"(\\(?:sub)*section\{)(?:\d+(?:\.\d+)*\.?\s*)?(.*?)\}", r"\1\2}", s)

            s = s.replace("~ ", "~")

            tex_lines[i] = s

    # @staticmethod
    # def clear_left_bracket(enviroment, text):
    #     regex_pattern = "(\\\\" + enviroment + "\\{)([^\\p{L}\\\\])"
    #     while regex.search(regex_pattern, text):
    #         text = regex.sub(regex_pattern, "\\2\\1", text, count=1)
    #     return text

    @staticmethod
    def clear_left_bracket(environment, text):
        regex_pattern = r"(\\" + regex.escape(environment) + r"\{)(\s*)"
        text = regex.sub(regex_pattern, r"\2\1", text)
        return text

    # @staticmethod
    # def clear_right_bracket(enviroment, text):
    #     regex_pattern = "(\\\\" + enviroment + "\\{.{0,}?)([^\\p{L}0-9\\.])(\\})"
    #     return regex.sub(regex_pattern, "\\1\\3\\2", text, count=1)

    @staticmethod
    def clear_right_bracket(environment, text):
        regex_pattern = r"(\\{env}\{{[^}}]*?)(~|\s*)(\}}+)".format(env=environment)
        text = regex.sub(regex_pattern, r"\1\3\2", text)
        return text


class BibFileCleaner:
    fields_to_remove = [
        'month',
        'file',
        'abstract',
        'copyright',
        'language',
        'isbn',
        'issn',
        'keywords',
        'date',
        'day',
    ]

    def __init__(self):
        self.cleaned_content = []

    def normalize_key(self, line):
        """Normalize the BibTeX entry key by removing non-ASCII characters."""
        match = regex.match(r'(@\w+{)([^,]+)', line)
        if match:
            entry_type = match.group(1)
            original_key = match.group(2)

            normalized_key = unicodedata.normalize('NFD', original_key)
            normalized_key = normalized_key.encode('ascii', 'ignore').decode('utf-8')
            normalized_key = regex.sub(r'[^\w]', '', normalized_key)

            line = entry_type + normalized_key + line[len(entry_type) + len(original_key):]

        return line

    def escape_latex_symbols(self, line):
        """Escape LaTeX-specific symbols in text."""
        replacements = {
            "&": r"\&",
            # I've excluded some potentially ill-behaving symbols for the reasons listed below:
            # "%": r"\%", # might occur in urls
            # "#": r"\#", # not sure about it
            # "_": r"\_", # might occur in entry key
            # "~": r"\textasciitilde", # might be on purpose (non breaking space)
            # "^": r"\textasciicircum" # rather rare and easy to spot, re.sub would potentially mess the entry
        }

        for symbol, replacement in replacements.items():
            line = regex.sub(r'(?<!\\)' + regex.escape(symbol), replacement, line)

        if line.count('$') % 2 != 0:
            line = regex.sub(r'(?<!\\)\$', r'\$', line)

        return line

    def clean_bib_content(self, bib_content):
        inside_removed_field = False
        for line in bib_content:
            if line.strip().startswith('@'):
                line = self.normalize_key(line)

            if any(line.strip().startswith(field) for field in self.fields_to_remove):
                inside_removed_field = True

            if inside_removed_field and (
                    line.strip().endswith('},') or line.strip().endswith('}') or line.strip().endswith(',')):
                inside_removed_field = False
                continue

            if not inside_removed_field:
                line = regex.sub(r'(\b\w+)=([0-9]+)', r'\1={\2}', line)
                line = self.escape_latex_symbols(line)
                self.cleaned_content.append(line)

        return self.cleaned_content
