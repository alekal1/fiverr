import xlrd

wb = xlrd.open_workbook('./input/example.xls')
wb_sheet = wb.sheet_by_index(0)

print(wb_sheet.cell_value(12, 1))