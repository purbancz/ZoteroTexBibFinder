from PySimpleGUI import Window, Input, FileBrowse, FolderBrowse, Button, WINDOW_CLOSED, Text


def create_gui(main_function):
    layout = [
        [Text('Select your .tex file:'), Input(), FileBrowse()],
        [Text('Select your .bib file:'), Input(), FileBrowse()],
        [Text('Enter the output file name:'), Input()],
        [Text('Select a folder to save the output file:'), Input(), FolderBrowse()],
        [Button('Submit'), Button('Cancel')]
    ]

    window = Window('Zotero made TeX BiB Finder', layout)

    while True:
        event, values = window.read()
        if event == 'Submit':
            tex_file = values[0]
            bib_file = values[1]
            output_file_name = values[2]
            output_folder = values[3]
            new_tex_file = output_folder + '/' + output_file_name
            main_function(tex_file, bib_file, new_tex_file)
        if event == WINDOW_CLOSED or event == 'Cancel':
            break

    window.close()
