import time

import pandas as pd

from excel_data_handler import ExcelDataHandler
from google_sheets_handler import GoogleSheetsHandler


class DataTransferManager:
    def __init__(self, excel_file_path, spreadsheet_id):
        self.excel_handler = ExcelDataHandler(excel_file_path)
        self.sheets_handler = GoogleSheetsHandler(spreadsheet_id)

    def transfer_data_to_sheets(self, excel_sheet_name):
        """Transfer data from an Excel sheet to a Google Sheets document."""
        data = self.excel_handler.get_sheet_data(excel_sheet_name)

        batch_size = 50
        batch_data = []

        for index, row in data.iterrows():
            time_value = row.get('Time', '')
            if pd.isna(time_value):
                time_value = ''
            else:
                time_value = str(time_value)

            name_value = row.get('Name', '')
            if pd.isna(name_value):
                name_value = ''
            else:
                name_value = str(name_value)

            description_value = row.get('Description', '')
            if pd.isna(description_value):
                description_value = ''
            else:
                description_value = str(description_value)

            batch_data.append([time_value, '', name_value, description_value])

            if len(batch_data) >= batch_size:
                self.sheets_handler.append_rows('Sheet1!A4', batch_data)
                time.sleep(1)
                batch_data = []

        if batch_data:
            self.sheets_handler.append_rows('Sheet1!A4', batch_data)

    def clear_google_sheets_range(self, google_sheets_range):
        """Clear a specific range in the Google Sheets document."""
        self.sheets_handler.clear_data_and_formatting(google_sheets_range)


# Usage example
if __name__ == "__main__":
    excel_file_path = '/home/nox/Культура.xlsx'
    spreadsheet_id = '1zkl-E_xhupjfUbWbJU-4iHWdxvoOMBklOm4-gyg5cAg'

    manager = DataTransferManager(excel_file_path, spreadsheet_id)

    # Transfer data from "Events" sheet in Excel to "Sheet1!A1:C10" in Google Sheets
    # manager.transfer_data_to_sheets('Events')

    # Clear a range in Google Sheets
    manager.clear_google_sheets_range('Sheet1!A4:L')
