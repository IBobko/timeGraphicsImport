import unittest

from data_transfer.excel_data_handler import ExcelDataHandler


class TestExcelDataHandler(unittest.TestCase):
    def setUp(self):
        """Set up the test environment with the real Excel file."""
        self.excel_file_path = '../test_file.xlsx'
        self.handler = ExcelDataHandler(self.excel_file_path)

    def test_get_sheet_names(self):
        """Test that sheet names are returned correctly."""
        sheet_names = self.handler.get_sheet_names()
        expected_sheets = {'Events',
                           'Google Analytics',
                           'Groups',
                           'Periods',
                           'Progresses',
                           'Reportings',
                           'Statistics',
                           'Timeline',
                           'Yandex Metrika'}
        self.assertEqual(expected_sheets, set(sheet_names))

    def test_get_sheet_data(self):
        """Test getting data from a specific sheet."""
        events_data = self.handler.get_sheet_data('Events')
        # Здесь вы можете указать ожидаемые размеры и данные на листе
        self.assertGreater(events_data.shape[0], 0)  # Проверяем, что на листе есть данные
        self.assertIn('Event', events_data.columns)  # Проверяем, что колонка 'Event' присутствует

    def test_get_range_data(self):
        """Test getting a specific range of data."""
        range_data = self.handler.get_range_data('Events', start_row=0, end_row=5, start_col=0, end_col=3)
        self.assertEqual(range_data.shape, (3, 3))

    def test_invalid_sheet_name(self):
        """Test that accessing an invalid sheet name raises an error."""
        with self.assertRaises(ValueError):
            self.handler.get_sheet_data('InvalidSheet')


if __name__ == "__main__":
    unittest.main()
