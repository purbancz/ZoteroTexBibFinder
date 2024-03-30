from PySimpleGUI import Window, Input, FileBrowse, FolderBrowse, Button, WINDOW_CLOSED, Text

layout = [
    [Text('Select your .tex file:'), Input(), FileBrowse()],
    [Text('Select your .bib file:'), Input(), FileBrowse()],
    [Text('Select a folder to save the output file:'), Input(), FolderBrowse()],
    [Text('Enter the output .tex file name:'), Input()],
    [Text('Enter the output .bib file name:'), Input()],
    [Button('Submit'), Button('Cancel')]
]


def create_gui(main_function):
    window = Window('Zotero made TeX BiB Finder', layout)

    while True:
        event, values = window.read()
        if event == 'Submit':
            tex_file = values[0]
            bib_file = values[1]
            output_folder = values[2]
            output_file_name = values[3]
            output_bib_file_name = values[4]
            new_tex_file = output_folder + '/' + output_file_name
            output_bib_file_name = output_folder + '/' + output_bib_file_name
            main_function(tex_file, bib_file, new_tex_file, output_bib_file_name)
        if event == WINDOW_CLOSED or event == 'Cancel':
            break

    window.close()
