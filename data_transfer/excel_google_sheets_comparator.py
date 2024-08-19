import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

class ExcelGoogleSheetsComparator:
    def __init__(self, google_sheet_id, excel_path, sheet_name, columns):
        self.google_sheet_id = google_sheet_id
        self.excel_path = excel_path
        self.sheet_name = sheet_name
        self.columns = columns
        self.client = self.authenticate_google_client()

    def authenticate_google_client(self):
        """Authenticate with Google API and return a client object."""
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name('your_credentials_file.json', scope)
        client = gspread.authorize(creds)
        return client

    def load_data(self):
        """Load data from Google Sheets and Excel file into pandas DataFrames."""
        # Load from Google Sheets
        worksheet = self.client.open_by_key(self.google_sheet_id).sheet1
        data_google = pd.DataFrame(worksheet.get_all_records())

        # Load from Excel
        data_excel = pd.read_excel(self.excel_path, sheet_name=self.sheet_name)

        # Filter columns
        data_google = data_google[self.columns]
        data_excel = data_excel[self.columns]

        return data_google, data_excel

    def compare_data(self):
        """Compare data and print differences."""
        data_google, data_excel = self.load_data()

        # Compare data
        merged = data_google.merge(data_excel, indicator=True, how='outer', suffixes=('_google', '_excel'))
        differences = merged[merged['_merge'] != 'both']

        # Output results
        if not differences.empty:
            print("Differences found:")
            print(differences)
        else:
            print("No differences found.")

# Example usage
if __name__ == "__main__":
    comparator = ExcelGoogleSheetsComparator(
        google_sheet_id='your_google_sheet_id',
        excel_path='/path/to/your/file.xlsx',
        sheet_name='Sheet1',
        columns=['Column1', 'Column2', 'Column3']
    )
    comparator.compare_data()
