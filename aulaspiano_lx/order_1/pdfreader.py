import os
import re
import csv
try:
    from docx2python import docx2python
    from io import StringIO
    from pdfminer.converter import TextConverter
    from pdfminer.layout import LAParams
    from pdfminer.pdfdocument import PDFDocument
    from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
    from pdfminer.pdfpage import PDFPage
    from pdfminer.pdfparser import PDFParser
except ModuleNotFoundError:
    os.system("pip install pdfminer")
    os.system("pip install docx2python")

emails = []


def extract_email(line, file_name, type):
    regex = re.compile(("([a-z0-9!#$%&'*+\/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+\/=?^_`"
                        "{|}~-]+)*(@|\sat\s)(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?(\.|"
                        "\sdot\s))+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?)"))
    match = re.search(regex, line)
    if match:
        list = []
        if type == 'pdf':
            list = [file_name.replace('.pdf', ''), f"{match.group(0)}"]
        elif type == 'doc':
            list = [file_name.replace('.doc', ''), f"{match.group(0)}"]
        elif type == 'docx':
            list = [file_name.replace('.docx', ''), f"{match.group(0)}"]
        emails.append(list)


def write_csv():
    print(emails)
    with open('email.csv', 'w', newline="") as file:
        writer = csv.writer(file)
        writer.writerows(emails)


def extract_information(pdf_file):
    _, type = os.path.splitext(f"cv/{pdf_file}")
    if type == ".pdf":
        output_string = StringIO()
        with open(f"cv/{pdf_file}", "rb") as file:
            parser = PDFParser(file)
            doc = PDFDocument(parser)
            manager = PDFResourceManager()
            device = TextConverter(manager, output_string, laparams=LAParams())
            interpreter = PDFPageInterpreter(manager, device)
            for page in PDFPage.create_pages(doc):
                interpreter.process_page(page)
            extract_email(output_string.getvalue(), pdf_file, 'pdf')
    elif type == ".doc" or type == '.docx':
        try:
            res = docx2python(f"cv/{pdf_file}")
            for elem in res.body:
                if type == '.docx':
                    extract_email(str(elem), pdf_file, 'docx')
                elif type == '.doc':
                    extract_email(str(elem), pdf_file, 'doc')
        except:
            pass


if __name__ == '__main__':
    for filename in os.listdir('cv'):
        extract_information(filename)
    write_csv()
    print('Done! Emails are available in email.csv file in the same directory!')
