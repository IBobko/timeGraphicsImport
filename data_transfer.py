import time

import pandas as pd
import colorsys

from excel_data_handler import ExcelDataHandler
from google_sheets_handler import GoogleSheetsHandler


class DataTransferManager:
    def __init__(self, excel_file_path, spreadsheet_id):
        self.excel_handler = ExcelDataHandler(excel_file_path)
        self.sheets_handler = GoogleSheetsHandler(spreadsheet_id)

    @staticmethod
    def get_cleaned_value(row, column_name):
        """Retrieve and clean a value from a DataFrame row based on the column name."""
        value = row.get(column_name, '')
        if pd.isna(value):
            return ''
        return str(value)

    @staticmethod
    def hsl_to_hex(h, s, l):
        """Convert HSL color to HEX."""
        r, g, b = colorsys.hls_to_rgb(h, l, s)
        return f'#{int(r * 255):02x}{int(g * 255):02x}{int(b * 255):02x}'

    def transfer_events_to_sheets(self):
        """Transfer data from the 'Events' sheet in Excel to the Google Sheets document."""
        data = self.excel_handler.get_sheet_data('Events')

        batch_size = 50
        batch_data = []
        position_toggle = True  # Start with 'top'

        # Initialize starting hue and increment
        start_hue = 0.0  # Hue range is [0.0, 1.0]
        hue_increment = 0.1  # Increment for each step

        for index, row in data.iterrows():
            time_value = self.get_cleaned_value(row, 'Time')
            name_value = self.get_cleaned_value(row, 'Name')
            description_value = self.get_cleaned_value(row, 'Description')

            # Determine the position value: 'top' or 'bottom'
            position_value = 'top' if position_toggle else 'bottom'

            # Toggle the position for the next iteration
            position_toggle = not position_toggle

            # Calculate the current color based on the hue
            current_hue = (start_hue + hue_increment * index) % 1.0
            color_value = self.hsl_to_hex(current_hue, 1.0, 0.5)  # Full saturation, medium lightness

            # Define rectangle type (e.g., 'smallrect')
            rect_type = 'rect'

            # Define text color
            text_color = '#000000'  # Default to black

            # Append the row to the batch
            batch_data.append(
                [time_value, '', name_value, description_value, '', '', position_value, rect_type, color_value,
                 text_color])

            if len(batch_data) >= batch_size:
                self.sheets_handler.append_rows('Sheet1!A4', batch_data)
                time.sleep(1)
                batch_data = []

        if batch_data:
            self.sheets_handler.append_rows('Sheet1!A4', batch_data)

    def transfer_periods_to_sheets(self):
        """Transfer data from the 'Periods' sheet in Excel to the Google Sheets document."""
        data = self.excel_handler.get_sheet_data('Periods')

        batch_size = 50
        batch_data = []
        position_toggle = True  # Start with 'top'

        # Initialize starting hue and increment
        start_hue = 0.0  # Hue range is [0.0, 1.0]
        hue_increment = 0.1  # Increment for each step

        for index, row in data.iterrows():
            start_time_value = self.get_cleaned_value(row, 'Time from')
            end_time_value = self.get_cleaned_value(row, 'Time to')
            name_value = self.get_cleaned_value(row, 'Name')
            description_value = self.get_cleaned_value(row, 'Description')

            # Determine the position value: 'top' or 'bottom'
            position_value = 'top' if position_toggle else 'bottom'

            # Toggle the position for the next iteration
            position_toggle = not position_toggle

            # Calculate the current color based on the hue
            current_hue = (start_hue + hue_increment * index) % 1.0
            color_value = self.hsl_to_hex(current_hue, 1.0, 0.5)  # Full saturation, medium lightness

            # Append the row to the batch
            batch_data.append([
                start_time_value, end_time_value, name_value, description_value, '', '', position_value, 'smallrect',
                color_value, '#000000'
            ])

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

    # Clear a range in Google Sheets
    manager.clear_google_sheets_range('Sheet1!A4:L')

    # Transfer data from "Events" sheet in Excel to "Sheet1!A1:C10" in Google Sheets
    manager.transfer_events_to_sheets()
    # Transfer data from "Periods" sheet in Excel to "Sheet1!A1:C10" in Google Sheets
    # manager.transfer_periods_to_sheets()
