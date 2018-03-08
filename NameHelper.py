#! python3

# author: Robin Modisch
# This tool is used to aid in renaming a lot of PDFs


import glob
import os
from pathlib import Path

from PyPDF2 import PdfFileReader as Reader


# TODO: PDFMiner3k as better text extraction?

# ------------ Funktions -----------------


def user_input():
    while True:
        folder_path = input("Input path to book folder:\n>")

        if folder_path == "":
            print("Goodbye")
            exit(0)

        file_list = glob.glob(folder_path + "\\*.pdf")

        if not file_list:  # empty lists are "False"
            print("no PDFs in that directory, try again")
        else:
            break
    return file_list


def gen_title(pdf):
    # lucky, easy correction if wanted
    if pdf.documentInfo.title:
        temp_title = pdf.documentInfo.title
        print("Embedded title found: {}".format(temp_title))
        prompt = input("Use it to rename? [Y, N]\n>")
        if prompt.upper() == "Y":
            return temp_title, "auto"

    # manual (human) parsing needed
    title = pdf.getPage(1).extractText().replace("\n", " ").strip()  # get cleaned title page

    print("current: {}: \nparsed frontpage-text:\n{}".format(book, title))
    title = input("Input new file name if desired, leave blank if not:\n>")

    if title:
        return title, "manual"
    else:
        print("Skipping file")
        return None, "skipped"


# --------------------- Main ----------------------

pdf_list = user_input()

counter = {"auto": 0, "manual": 0, "skipped": 0}

# iterate through list of titles
for file in pdf_list:
    pdf = Reader(file, strict=True)

    p = Path(file)
    book = p.stem
    base_path = p.parent

    new_name, type_ = gen_title(pdf)

    counter[type_] += 1

    if not new_name:
        continue

    new_file = str(base_path.joinpath(new_name + ".pdf"))
    os.rename(file, new_file)
    print("file {} has been renamed to {}".format(file, new_file))

print("Done!\n Auto:    {:2}\n Manual:  {:2}\n Skipped: {:2}"
      .format(counter["auto"], counter["manual"], counter["skipped"]))
