# Zotero+OpenOffice made TeX BiB Finder



[![github](https://img.shields.io/badge/GitHub-purbancz-181717.svg?style=flat&logo=github)](https://github.com/purbancz)
[![X](https://img.shields.io/badge/twitter-@purbancz-00aced.svg?style=flat&logo=X)](https://twitter.com/purbancz)
[![linkedin](https://img.shields.io/badge/LinkedIn-Piotr_Urbańczyk-00aced.svg?style=flat&logo=linkedin)](https://www.linkedin.com/in/piotr-urba%C5%84czyk-9943ab17a/)
[![website](https://img.shields.io/badge/Website-Piotr_Urbańczyk-5087B2.svg?style=flat&logo=data:image/svg%2bxml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHg9IjBweCIgeT0iMHB4IiB3aWR0aD0iMTAwIiBoZWlnaHQ9IjEwMCIgdmlld0JveD0iMCAwIDI0IDI0Ij4KICAgIDxwYXRoIGQ9Ik0gMTIgMi4wOTk2MDk0IEwgMSAxMiBMIDQgMTIgTCA0IDIxIEwgMTAgMjEgTCAxMCAxNCBMIDE0IDE0IEwgMTQgMjEgTCAyMCAyMSBMIDIwIDEyIEwgMjMgMTIgTCAxMiAyLjA5OTYwOTQgeiIgZmlsbD0iI2ZmZiI+PC9wYXRoPgo8L3N2Zz4=)](https://www.copernicuscenter.edu.pl/en/person/urbanczyk-piotr-2/)

## Description
This application is designed to help you find and clean up BibTeX references in your LaTeX files. The `.tex`
files are generated automatically using an OpenOffice plugin on files containing a Zotero made bibliography.
The application uses a simple GUI to select your `.tex` and `.bib` files, and outputs a new `.tex` file
with the cleaned up references.

This code was created as part of the design workshop of the Languages and Libraries of Data Analysis course
with Dr. Marek Gajęcki at the Faculty of Computer Science of the AGH University of Cracow.

## Installation
1. Clone this repository: `git clone https://github.com/purbancz/ZoteroTexBibFinder.git`
2. Navigate to the cloned repository: `cd ZoteroTexBibFinder`
3. Install the required packages: `pip install -r requirements.txt`

## Usage
1. Run the application: `python main.py`
2. In the GUI, select your `.tex` file, `.bib` file, output file name, and output folder.
3. Click 'Submit' to start the process. The application will create a new `.tex` file in the specified output folder.

## Dependencies
This application requires the following Python packages:
- PySimpleGUI

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

