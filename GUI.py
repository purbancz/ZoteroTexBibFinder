from PySimpleGUI import Window, Input, FileBrowse, Button, WINDOW_CLOSED, Text, FileSaveAs

layout = [
    [Text('Select your .tex file:'), Input(), FileBrowse()],
    [Text('Select your .bib file:'), Input(), FileBrowse()],
    [Text('Select the output .tex file:'), Input(), FileSaveAs("Save As", file_types=(("TeX Files", "*.tex"),))],
    [Text('Select the output .bib file:'), Input(), FileSaveAs("Save As", file_types=(("BibTeX Files", "*.bib"),))],
    [Button('Submit'), Button('Cancel')]
]


def create_gui(main_function):
    window = Window('Zotero made TeX BiB Finder', layout)

    while True:
        event, values = window.read()
        if event == 'Submit':
            tex_file = values[0]
            bib_file = values[1]
            output_tex_file = values[2]
            output_bib_file = values[3]
            if tex_file and bib_file and output_tex_file and output_bib_file:
                main_function(tex_file, bib_file, output_tex_file, output_bib_file)
            else:
                print("Please make sure all files are selected.")
        if event == WINDOW_CLOSED or event == 'Cancel':
            break

    window.close()
