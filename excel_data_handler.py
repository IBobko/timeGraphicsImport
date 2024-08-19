import pandas as pd


class ExcelDataHandler:
    def __init__(self, excel_file_path):
        self.excel_file_path = excel_file_path
        self.all_sheets = self._load_excel_file()

    def _load_excel_file(self):
        """Private method to load the Excel file."""
        return pd.read_excel(self.excel_file_path, sheet_name=None)

    def get_sheet_names(self):
        """Return the names of all sheets in the Excel file."""
        return self.all_sheets.keys()

    def get_sheet_data(self, sheet_name):
        """Return the data of the specified sheet."""
        if sheet_name in self.all_sheets:
            return self.all_sheets[sheet_name]
        else:
            raise ValueError(f"Sheet '{sheet_name}' does not exist in the Excel file.")

    def print_sheet_head(self, sheet_name, n=5):
        """Print the first few rows of the specified sheet."""
        data = self.get_sheet_data(sheet_name)
        print(data.head(n))

    def get_range_data(self, sheet_name, start_row, end_row, start_col, end_col):
        """Return the data from a specified range in the sheet."""
        data = self.get_sheet_data(sheet_name)

        # Selecting the specified range of rows and columns
        range_data = data.iloc[start_row:end_row, start_col:end_col]

        return range_data


# Usage example
if __name__ == "__main__":
    excel_file_path = '/home/nox/Культура.xlsx'
    excel_handler = ExcelDataHandler(excel_file_path)

    # Print the first few rows of the "Events" sheet
    # excel_handler.print_sheet_head('Events')
    #
    # # Print the first few rows of the "Periods" sheet
    # excel_handler.print_sheet_head('Periods')

    # Get data from a specific range in the "Events" sheet
    range_data = excel_handler.get_range_data('Events', start_row=1, end_row=767, start_col=0, end_col=3)
    print(range_data)

