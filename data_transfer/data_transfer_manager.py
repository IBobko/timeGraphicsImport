import pandas as pd
import time
import colorsys
from .excel_data_handler import ExcelDataHandler
from .google_sheets_handler import GoogleSheetsHandler


class DataTransferManager:
    def __init__(self, excel_file_path, spreadsheet_id, auth):
        self.excel_handler = ExcelDataHandler(excel_file_path)
        self.sheets_handler = GoogleSheetsHandler(auth, spreadsheet_id)

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
        start_hue = 0.0  # Hue range is [0.0, 1.0]
        hue_increment = 0.1  # Increment for each step
        for index, row in data.iterrows():
            time_value = self.get_cleaned_value(row, 'Time')
            name_value = self.get_cleaned_value(row, 'Name')
            description_value = self.get_cleaned_value(row, 'Description')
            position_value = 'top' if position_toggle else 'bottom'
            position_toggle = not position_toggle
            current_hue = (start_hue + hue_increment * index) % 1.0
            color_value = self.hsl_to_hex(current_hue, 1.0, 0.5)  # Full saturation, medium lightness
            rect_type = 'rect'
            text_color = '#000000'  # Default to black
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
            batch_data.append(
                [start_time_value, end_time_value, name_value, description_value, '', '', position_value, 'smallrect',
                 color_value, '#000000'])
            if len(batch_data) >= batch_size:
                self.sheets_handler.append_rows('Sheet1!A4', batch_data)
                time.sleep(1)
                batch_data = []
        if batch_data:
            self.sheets_handler.append_rows('Sheet1!A4', batch_data)

    def clear_google_sheets_range(self, google_sheets_range):
        """Clear a specific range in the Google Sheets document."""
        self.sheets_handler.clear_data_and_formatting(google_sheets_range)

    @classmethod
    def compare_excel_files(cls, excel_file_path1, excel_file_path2, sheet_name):
        """Compares sheets with the same name from two Excel files and prints added rows."""
        try:
            # Загружаем данные из Excel-файлов
            data1 = pd.read_excel(excel_file_path1, sheet_name=sheet_name)
            data2 = pd.read_excel(excel_file_path2, sheet_name=sheet_name)

            # Сброс индексов, если порядок строк не важен
            data1.reset_index(drop=True, inplace=True)
            data2.reset_index(drop=True, inplace=True)

            # Получаем строки, которые есть в data2, но нет в data1
            merged = data2.merge(data1, indicator=True, how='outer')
            added_rows = merged[merged['_merge'] == 'left_only']

            # Выводим информацию о добавленных строках
            if not added_rows.empty:
                print("Added rows:")
                print(added_rows)
            else:
                print("No rows have been added.")

        except Exception as e:
            print("An error occurred:", e)
