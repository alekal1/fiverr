import xlrd
import xlsxwriter

FILE_TO_BE_FILLED = './excel_files/Data set - to be filled.xlsx'
CONTROL_OF_CORRUPTION = './excel_files/control of corruption.xlsx'


def get_country_coodrinates(sheet):
    countries = {}
    for i in range(3, sheet.nrows):
        coordinate_list = []
        temp_list = []
        if sheet.cell_value(i, 0) not in countries:
            countries[sheet.cell_value(i, 0)] = [[i, 0]]
        else:
            countries[sheet.cell_value(i, 0)].append([i, 0])
    return countries


# def get_country_rows_coordinates(sheet):
#     countries = {}
#     for i in range(3, sheet.nrows):
#         if sheet.cell_value(i, 0) not in countries:
#             countries[sheet.cell_value(i, 0)] = 1
#         else:
#             countries[sheet.cell_value(i, 0)] += 1
#     return countries


def get_corruption(sheet):
    corruption_per_country = {}
    for row in range(1, 215):
        temp = []
        # sheet.cell_value(row, 0) - Country
        for column in range(4, 19):
            temp.append(sheet.cell_value(row, column))
        corruption_per_country[sheet.cell_value(row, 0)] = temp
    return corruption_per_country


def fill_corruption_index(sheet, countries, corruption_list):
    workbook = xlsxwriter.Workbook(FILE_TO_BE_FILLED)
    for i in range(0, len(corruption_list)):
        for elem in countries:
            for c in countries[elem]:
                workbook.write(c[0], 8, corruption_list[i])
                # sheet.cell_value(c[0], 8) == corruption_list[i]


if __name__ == '__main__':
    dataset_to_be_filled = xlrd.open_workbook(FILE_TO_BE_FILLED)
    data_sheet = dataset_to_be_filled.sheet_by_index(0)
    country_coordinates = get_country_coodrinates(data_sheet)


    corruption_wb = xlrd.open_workbook(CONTROL_OF_CORRUPTION)
    corruption_sheet = corruption_wb.sheet_by_index(0)
    corruption_list = get_corruption(corruption_sheet)

    fill_corruption_index(data_sheet, country_coordinates, corruption_list)