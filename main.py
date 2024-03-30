from cleaners import DummyLinesCleaner, DummyCharactersCleaner, BibFileCleaner
from model import BibParser, BibFinder, SanityCheck
from utils import TexParser, SaveFile
from GUI import create_gui


def main(tex_file, bib_file, new_tex_file, new_bib_file):
    parser = TexParser()
    lines_cleaner = DummyLinesCleaner()
    characters_cleaner = DummyCharactersCleaner()
    bib_parser = BibParser()
    bib_finder = BibFinder()
    sanity_check = SanityCheck()
    bib_cleaner = BibFileCleaner()
    saver = SaveFile()

    tex_lines = parser.parse_tex_file(tex_file)
    tex_lines = lines_cleaner.clean_dummy_lines(tex_lines)
    characters_cleaner.clear_dummy_characters(tex_lines)
    bib_entries = bib_parser.parse_bib_file(bib_file)
    tex_lines = bib_finder.find_bib_references(tex_lines, bib_entries)
    tex_lines = sanity_check.check_and_update_content(tex_lines)

    bib_lines = parser.parse_tex_file(bib_file)
    new_bib_lines = bib_cleaner.clean_bib_content(bib_lines)

    for line in tex_lines:
        print(line)

    for entry in bib_entries:
        print(entry)

    saver.rewrite_file(new_tex_file, tex_lines)
    saver.rewrite_file_single_par(new_bib_file, new_bib_lines)


if __name__ == "__main__":
    create_gui(main)
    # tex_file = "oleksowicz_org.tex"
    # new_tex_file = "oleksowicz.tex"
    # bib_filename = "Oleksowicz.bib"
    # main(tex_file, bib_filename, new_tex_file)
