from pathlib import Path
import glob

from PyPDF2 import PdfFileReader as rd


for file in glob.glob("U:\\PDF\\*.pdf"):
    pdf = rd(file)
    title = pdf.getPage(1).extractText().strip().replace("\n", " ")
    book = Path(file).stem
    print("{}: {}".format(book, title))


# iterate through list of titles
# show ID & all extracted texts of first page [correct large blanks to single blanks]
# show input to fill "human-parsed" title into
# if empty skip file
# else rename file to new title

