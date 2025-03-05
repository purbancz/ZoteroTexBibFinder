import tkinter as tk
from tkinter import filedialog, messagebox


def create_gui(main_function):
    def submit_action():
        tex_file = tex_entry.get()
        bib_file = bib_entry.get()
        output_tex_file = tex_output_entry.get()
        output_bib_file = bib_output_entry.get()

        if tex_file and bib_file and output_tex_file and output_bib_file:
            main_function(tex_file, bib_file, output_tex_file, output_bib_file)
            messagebox.showinfo("Success", "Operation Successful!")
        else:
            messagebox.showerror("Error", "Please make sure all files are selected.")

    def browse_tex_file():
        filename = filedialog.askopenfilename(filetypes=[("TeX Files", "*.tex")])
        tex_entry.delete(0, tk.END)
        tex_entry.insert(0, filename)

    def browse_bib_file():
        filename = filedialog.askopenfilename(filetypes=[("BibTeX Files", "*.bib")])
        bib_entry.delete(0, tk.END)
        bib_entry.insert(0, filename)

    def save_tex_file():
        filename = filedialog.asksaveasfilename(defaultextension=".tex", filetypes=[("TeX Files", "*.tex")])
        tex_output_entry.delete(0, tk.END)
        tex_output_entry.insert(0, filename)

    def save_bib_file():
        filename = filedialog.asksaveasfilename(defaultextension=".bib", filetypes=[("BibTeX Files", "*.bib")])
        bib_output_entry.delete(0, tk.END)
        bib_output_entry.insert(0, filename)

    # Create the main window
    root = tk.Tk()
    root.title("Zotero made TeX BiB Finder")

    # Layout for .tex file selection
    tk.Label(root, text="Select your .tex file:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
    tex_entry = tk.Entry(root, width=40)
    tex_entry.grid(row=0, column=1, padx=5, pady=5)
    tk.Button(root, text="Browse", command=browse_tex_file).grid(row=0, column=2, padx=5, pady=5)

    # Layout for .bib file selection
    tk.Label(root, text="Select your .bib file:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
    bib_entry = tk.Entry(root, width=40)
    bib_entry.grid(row=1, column=1, padx=5, pady=5)
    tk.Button(root, text="Browse", command=browse_bib_file).grid(row=1, column=2, padx=5, pady=5)

    # Layout for output .tex file
    tk.Label(root, text="Select the output .tex file:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
    tex_output_entry = tk.Entry(root, width=40)
    tex_output_entry.grid(row=2, column=1, padx=5, pady=5)
    tk.Button(root, text="Save As", command=save_tex_file).grid(row=2, column=2, padx=5, pady=5)

    # Layout for output .bib file
    tk.Label(root, text="Select the output .bib file:").grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
    bib_output_entry = tk.Entry(root, width=40)
    bib_output_entry.grid(row=3, column=1, padx=5, pady=5)
    tk.Button(root, text="Save As", command=save_bib_file).grid(row=3, column=2, padx=5, pady=5)

    # Submit and Cancel buttons
    tk.Button(root, text="Submit", command=submit_action).grid(row=4, column=0, columnspan=2, pady=10)
    tk.Button(root, text="Cancel", command=root.quit).grid(row=4, column=2, pady=10)

    root.mainloop()
