import xlrd


class XlsReader:

    _data_path = f'data'

    def __init__(self, name, sheet=None):
        self._wb = xlrd.open_workbook(f'{self._data_path}/{name}')
        if sheet is not None:
            self._sheet = self._wb.sheet_by_name(sheet)
        else:
            self._sheet = self._wb.sheet_by_index(0)

    def read(self):
        chart_keys = self._sheet.col_values(0, 1, self._sheet.nrows)
        chart_labels = self._sheet.row_values(0, 1, self._sheet.ncols)
        chart_values = []
        for row in range(1, self._sheet.nrows):
            chart_values.append([])
            for column in range(1, self._sheet.ncols):
                chart_values[row - 1].append(self._get_cell_value(row, column))
        return chart_keys, chart_labels, chart_values

    def _get_cell_value(self, row, column):
        # 1 cell type : 0 empty,1 string, 2 number, 3 date, 4 boolean, 5 error
        if self._sheet.cell_type(row, column) == 0:
            return 0
        elif self._sheet.cell_type(row, column) == 1:
            try:
                if self._sheet.cell_value(row, column).find('.') >= 0:
                    return float(self._sheet.cell_value(row, column))
                else:
                    return int(self._sheet.cell_value(row, column))
            except ValueError:
                return 0
        elif self._sheet.cell_type(row, column) == 5:
            return 0
        else:
            return self._sheet.cell_value(row, column)
