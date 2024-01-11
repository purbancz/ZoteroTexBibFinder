from cleaners import DummyLinesCleaner, DummyCharactersCleaner
from model import BibParser, BibFinder
from utils import TexParser, SaveFile
from GUI import create_gui


def main(tex_file, bib_file, new_tex_file):

    parser = TexParser()
    saver = SaveFile()
    lines_cleaner = DummyLinesCleaner()
    characters_cleaner = DummyCharactersCleaner()
    bib_parser = BibParser()
    bib_finder = BibFinder()

    tex_lines = parser.parse_tex_file(tex_file)
    tex_lines = lines_cleaner.clean_dummy_lines(tex_lines)
    characters_cleaner.clear_dummy_characters(tex_lines)
    bib_entries = bib_parser.parse_bib_file(bib_file)
    tex_lines = bib_finder.find_bib_references(tex_lines, bib_entries)

    for line in tex_lines:
        print(line)

    for entry in bib_entries:
        print(entry)

    saver.rewrite_file(new_tex_file, tex_lines)


if __name__ == "__main__":
    create_gui(main)
