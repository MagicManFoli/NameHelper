#! python3

# author: Robin Modisch
# This tool is used to aid in renaming a lot of PDFs


import glob
import shutil
from pathlib import Path

from PyPDF2 import PdfFileReader as Reader


# ------------ Functions -----------------


def user_input():
    """encapsulates file selection"""
    while True:
        folder_path = input("Input path to book folder:\n>")

        if folder_path == "":
            print("Goodbye")
            exit(0)

        file_list = glob.glob(folder_path + "\\*.pdf")  # TODO: check if non-recursive

        if not file_list:  # empty lists are "False"
            print("no PDFs in that directory, try again")
        else:
            break
    return file_list


# noinspection PyUnresolvedReferences
def gen_title(file):
    """used to get a valid title by all means, categorises"""

    pdf = Reader(file, strict=True)

    # lucky, easy correction if wanted
    if pdf.documentInfo.title:
        emb_title = str(pdf.documentInfo.title).strip()
        print("Embedded title found: {}".format(emb_title))
        prompt = input("Use it to rename? [Y, N]\n>")
        if prompt.upper() == "Y":
            return emb_title, "auto"

    # manual (human) parsing needed
    parsed_title = pdf.getPage(1).extractText().replace("\n", " ").strip()  # get cleaned title page

    # TODO: better commands, add option to cancel
    print("parsed frontpage-text:\n{}".format(parsed_title))
    title = input("Input new file name if desired, X to mark, leave blank to skip:\n>")

    title = title.replace(":", "").strip()  # TODO: Add more char corrections "\/.

    # dictionary-comparison with default as title?
    # TODO: better evaluation?
    if title:
        if title == "X":  # marked
            return Path(file).stem, "marked"
        else:  # new title
            return title, "manual"
    else:  # skipped
        print("Skipping file")
        return Path(file).stem, "skipped"


# --------------------- Main ----------------------

def main():
    counter = {"auto": 0, "manual": 0, "marked": 0, "skipped": 0}

    # list of files in user selected dir
    pdf_list = user_input()

    try:
        # iterate through list of titles
        for file in pdf_list:

            p = Path(file)
            file_name = p.stem
            base_path = p.parent

            print("current PDF: {}".format(file_name))

            # new or None
            gen_name, type_ = gen_title(file)

            counter[type_] += 1

            # TODO: move files to new folders

            # create dir to move file into
            move_path = base_path.joinpath(type_)
            Path(move_path).mkdir(parents=True, exist_ok=True)

            # append new name to change to if necessary
            # if gen_name != file_name:
            move_path = move_path.joinpath(gen_name + ".pdf")

            # TODO: check if file exists, if yes: append (2)
            # Path .exists?
            while move_path.exists():
                print("File {} already exists".format(move_path))
                move_path = move_path.parent / (move_path.stem + "_" + move_path.suffix)

            # if not Path(move_path):
            #     raise FileNotFoundError("File {} not found".format(move_path))

            # move or move + rename
            processed_name = shutil.move(file, move_path)

            print("file {} is now {}\n".format(file, processed_name))

    # generic catch to reformat exceptions for console output
    except Exception as e:
        print("An Error occurred:\n{}\n\n".format(e))  # TODO: Add (shortened) traceback

    print("Done!\n Auto:    {:2}\n Manual:  {:2}\n Marked:  {:2}\n Skipped: {:2}"
          .format(counter["auto"], counter["manual"], counter["marked"], counter["skipped"]))

    # prevent cmd to exit prematurely
    input("Press Enter to continue...\n")


# end of main


if __name__ == "__main__":
    main()

    # done
