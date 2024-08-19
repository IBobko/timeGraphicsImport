import os

import google_auth_oauthlib.flow
import googleapiclient.discovery
from dotenv import load_dotenv


class GoogleSheetsHandler:
    def __init__(self, spreadsheet_id):
        load_dotenv()
        self.CLIENT_SECRETS_FILE = os.getenv("GOOGLE_API_CREDENTIALS_PATH")
        self.SPREADSHEET_ID = spreadsheet_id
        self.SCOPES = [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive'
        ]
        self.service = self._authenticate()

    def _authenticate(self):
        """Authenticate and create the Google Sheets API service object."""
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            self.CLIENT_SECRETS_FILE, self.SCOPES)
        credentials = flow.run_local_server(port=0)
        return googleapiclient.discovery.build('sheets', 'v4', credentials=credentials)

    def read_data(self, range_name):
        """Read data from a specified range in the Google Sheets document."""
        sheet = self.service.spreadsheets()
        result = sheet.values().get(spreadsheetId=self.SPREADSHEET_ID, range=range_name).execute()
        values = result.get('values', [])

        if not values:
            print('No data found.')
        else:
            print(f"Data from range: {range_name}")
            for row in values:
                print(row)

    def clear_data(self, range_name):
        """Clear data from a specified range in the Google Sheets document."""
        clear_body = {}
        self.service.spreadsheets().values().clear(spreadsheetId=self.SPREADSHEET_ID, range=range_name,
                                                   body=clear_body).execute()
        print(f"Data cleared from range: {range_name}")

    def get_sheet_id_by_name(self, sheet_name):
        """Get the sheet ID from the sheet name."""
        sheets = self.service.spreadsheets().get(spreadsheetId=self.SPREADSHEET_ID).execute().get('sheets', [])
        for sheet in sheets:
            if sheet['properties']['title'] == sheet_name:
                return sheet['properties']['sheetId']
        raise ValueError(f'Sheet {sheet_name} not found')

    def clear_data_and_formatting(self, range_name):
        """Clear data and formatting from a specified range in the Google Sheets document."""
        sheet_id = self.get_sheet_id_by_name(range_name.split('!')[0])

        start_row_index = self.get_row_index(range_name)
        end_row_index = 10000
        start_column_index = self.get_column_index(range_name)
        end_column_index = 1000

        requests = [
            {
                "updateCells": {
                    "range": {
                        "sheetId": sheet_id,
                        "startRowIndex": start_row_index,
                        "endRowIndex": end_row_index,
                        "startColumnIndex": start_column_index,
                        "endColumnIndex": end_column_index
                    },
                    "fields": "userEnteredValue,userEnteredFormat"
                }
            }
        ]

        body = {
            'requests': requests
        }

        self.service.spreadsheets().batchUpdate(spreadsheetId=self.SPREADSHEET_ID, body=body).execute()
        print(f"Data and formatting cleared from range: {range_name}")

    def get_row_index(self, range_name, end=False):
        """Get the row index from the A1 range."""
        import re
        match = re.search(r'(\d+)', range_name.split('!')[1])
        if match:
            row_index = int(match.group(1)) - 1
            return row_index if not end else row_index
        return None

    def get_column_index(self, range_name, end=False):
        """Get the column index from the A1 range."""
        import re
        match = re.search(r'([A-Z]+)', range_name.split('!')[1])
        if match:
            column_index = self.column_to_index(match.group(1))
            return column_index if not end else column_index
        return None

    def column_to_index(self, column):
        """Convert column letter(s) to zero-based index."""
        index = 0
        for char in column:
            index = index * 26 + (ord(char) - ord('A') + 1)
        return index - 1

    def update_data(self, range_name, values):
        """Update data in a specified range in the Google Sheets document."""
        update_body = {
            'values': [values]
        }
        result = self.service.spreadsheets().values().update(
            spreadsheetId=self.SPREADSHEET_ID, range=range_name,
            valueInputOption='RAW', body=update_body).execute()

        print(f"{result.get('updatedCells')} cells updated.")

    def append_row(self, range_name, values):
        """Append a new row of data to the specified range in the Google Sheets document."""
        append_body = {
            'values': [values]
        }
        result = self.service.spreadsheets().values().append(
            spreadsheetId=self.SPREADSHEET_ID, range=range_name,
            valueInputOption='RAW', insertDataOption='INSERT_ROWS', body=append_body).execute()

        print(f"{result.get('updates').get('updatedCells')} cells appended.")

    def append_rows(self, range_name, values):
        """Append multiple rows of data to the specified range in the Google Sheets document."""
        append_body = {
            'values': values
        }
        result = self.service.spreadsheets().values().append(
            spreadsheetId=self.SPREADSHEET_ID, range=range_name,
            valueInputOption='RAW', insertDataOption='INSERT_ROWS', body=append_body).execute()
        print(f"{result.get('updates').get('updatedCells')} cells appended.")

    def list_excel_files(self):
        """List all Excel files in the user's Google Drive."""
        query = "mimeType='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' or mimeType='application/vnd.ms-excel'"
        results = self.service.files().list(
            q=query,
            pageSize=10,  # Adjust the size to list more or fewer files
            fields="nextPageToken, files(id, name)"
        ).execute()

        items = results.get('files', [])
        if not items:
            print('No Excel files found.')
        else:
            print('Excel files:')
            for item in items:
                print(f"{item['name']} (ID: {item['id']})")


# Usage example
if __name__ == "__main__":
    spreadsheet_id = '1zkl-E_xhupjfUbWbJU-4iHWdxvoOMBklOm4-gyg5cAg'

    sheets_handler = GoogleSheetsHandler(spreadsheet_id)

    sheets_handler.list_excel_files();

    # Example 1: Reading data
    # sheets_handler.read_data('Sheet1!A1:C2')

    # Clear data from a specific range
    # sheets_handler.clear_data('Sheet1!A4:L')

    # Example 2: Updating data
    # sheets_handler.update_data('Sheet1!B4', ['Updated Description'])

    # Example 3: Adding a new row
    # sheets_handler.append_row('Sheet1!A6', ['2000 1 1', 'New Event', 'New Description'])
