import regex


class BibEntries:
    def __init__(self, key, author, year):
        self.key = key
        self.author = author
        self.year = year
        self.title = None

    def __str__(self):
        return f"BibEntries [key={self.key}, author={self.author}, year={self.year}, title={self.title}]"


class BibReferences:
    def __init__(self, prefix, key, suffix):
        self.prefix = prefix
        self.key = key
        self.suffix = suffix

    def __str__(self):
        return f"[{self.prefix}][{self.suffix}]{{self.key}}"


class BibFinder:
    def __init__(self):
        self.tex_bib_lines = []
        self.regex = r"(\\label\{ref:RND[a-zA-Z0-9]{10}\})(\()([^\)]{4,})(\))([.,:;?!])?"

    def find_bib_references(self, tex_lines, bib_entries):
        for i in range(len(tex_lines)):
            prev_line = ""
            par = tex_lines[i]
            matcher = regex.finditer(self.regex, par)
            temporary_matcher_end = 0
            matches = [match for match in matcher]
            if not matches:
                self.tex_bib_lines.append(par)
            else:
                for match in matches:
                    try:
                        prev_line = par[0:match.start() - 1]
                    except Exception as e:
                        print(f"Something went wrong here: {prev_line}{par}")
                    self.tex_bib_lines.append(prev_line)
                    self.tex_bib_lines.append("%" + match.group())
                    try:
                        self.tex_bib_lines.append(
                            self.create_bib_entry(match.group(3), self.last_word(prev_line), bib_entries)
                            + self.de_nullifier(match.group(5))
                            + self.add_space(par, match.end())
                            + "%")
                    except Exception as e:
                        print(f"Something went wrong here: {prev_line}")
                    temporary_matcher_end = match.end()
                self.tex_bib_lines.append(par[temporary_matcher_end:len(par)])
        return self.tex_bib_lines

    def create_bib_entry(self, bib_entry_raw, one_word_before, bib_entries):
        bib_refs = []
        many_in_one_year = 0
        bib_references_text = bib_entry_raw.split("; ")
        if len(bib_references_text) == 1:
            bib_tex_formula = "\\parencite"
        else:
            bib_tex_formula = "\\parencites"
        for i in range(len(bib_references_text)):
            a_bc_entries = set()
            author = ""
            year = ""
            bib_ref = BibReferences("", "", "")
            bib_single_text_entry = bib_references_text[i].split(", ")
            for subs in bib_single_text_entry:
                if subs[0].isdigit():
                    year = subs.split(" ")[0]
                if subs[0].islower():
                    if year:
                        bib_ref.suffix = subs
                    else:
                        bib_ref.prefix = bib_ref.prefix + subs[0:self.first_upper_case(subs) - 1]
                        if author:
                            author = author + ", "
                        author = author + subs[self.first_upper_case(subs):].replace("[\\p{M}]", "")
                if subs[0].isupper():
                    if author:
                        author = author + ", "
                    author = author + subs
            if not author:
                bib_tex_formula = bib_tex_formula + "*"
                author = one_word_before
            if len(year) > 4 and year[4].isalpha():
                many_in_one_year = ord(year[4]) - 97
                year = year[0:len(year) - 1]
            while not a_bc_entries and len(author) > 0:
                for bib_entry in bib_entries:
                    if self.are_authors(author.split(", "), bib_entry.author) and bib_entry.year == year:
                        a_bc_entries.add(bib_entry)
                author = author[0:len(author) - 1]
            sorted_abc_list = sorted(list(a_bc_entries), key=lambda x: x.title)
            if not sorted_abc_list:
                bib_ref.key = ""
            else:
                bib_ref.key = sorted_abc_list[many_in_one_year].key
                many_in_one_year = 0
            bib_refs.append(bib_ref)
        for bib_final_ref in bib_refs:
            bib_tex_formula = bib_tex_formula + str(bib_final_ref)
        return bib_tex_formula

    @staticmethod
    def first_upper_case(str):
        for i in range(len(str)):
            if str[i].isupper():
                return i
        return 0

    @staticmethod
    def last_word(str):
        return str.split()[-1] if str else ""

    @staticmethod
    def de_nullifier(str):
        return str if str else ""

    @staticmethod
    def add_space(str, index):
        if index < len(str) and str[index].isspace():
            return " "
        else:
            return ""

    @staticmethod
    def are_authors(authors1, authors2):
        return set(authors1) == set(authors2.split(", "))


class BibParser:
    @staticmethod
    def parse_bib_file(path_to_file):
        list_bib_entries = []
        last_entry_start_line = 0
        with open(path_to_file, 'r', encoding="utf-8") as file:
            bib_lines = file.readlines()
        for i in range(len(bib_lines)):
            line = bib_lines[i].strip()
            if line.startswith("@"):
                key_line = line.split("{", 1)
                last_entry_start_line = i
                entry = BibEntries("", "", "")
                if len(key_line) > 1:
                    entry.key = key_line[1].split(",", 1)[0]
            if line.startswith("author"):
                key_author = line.split("{", 1)
                if len(key_author) > 1:
                    entry.author = key_author[1].rsplit("}", 1)[
                        0]
            if line.startswith("title"):
                key_title = line.split("{", 1)
                if len(key_title) > 1:
                    entry.title = key_title[1].rsplit("}", 1)[0]
            if line.startswith("year"):
                key_year = line.split("{", 1)
                if len(key_year) > 1:
                    entry.year = key_year[1].rsplit("}", 1)[0]
            if line == "}":
                if not entry.author:
                    for y in range(i, last_entry_start_line, -1):
                        line = bib_lines[y].strip()
                        if line.startswith("editor"):
                            key_author = line.split("{", 1)
                            if len(key_author) > 1:
                                entry.author = key_author[1].rsplit("}", 1)[
                                    0]
                            break
                if not entry.author:
                    entry.author = entry.title
                list_bib_entries.append(entry)
        return list_bib_entries