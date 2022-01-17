### START EXCEL UTILITIES

import openpyxl

def column_number_to_string(n):
    string = ""
    while n > 0:
        n, remainder = divmod(n - 1, 26)
        string = chr(65 + remainder) + string
    return string

def column_string_to_number(col):
    num = 0
    for c in col:
        if c in string.ascii_letters:
            num = num * 26 + (ord(c.upper()) - ord('A')) + 1
    return num

def create_excel_file():
    wb_obj = openpyxl.Workbook()

    sheets = wb_obj.sheetnames

    for sheet in sheets:
        std = wb_obj[sheet]

        wb_obj.remove(std)

    return wb_obj

def make_bold(sheet, cells):
    for cell in cells:
        sheet[cell].font = openpyxl.styles.Font(bold=True)

def fill_cells(sheet, cells, content):
    for x, y in zip(cells, content):
        sheet[x].value = y

def wrap_text(sheet, cell):
    sheet[cell].alignment = openpyxl.styles.Alignment(wrapText=True)