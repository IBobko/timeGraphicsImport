import gspread
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv
import os


class GoogleServiceAuth:
    def __init__(self):
        load_dotenv()
        self.service_creds_file = os.getenv("GOOGLE_API_SERVICE_CREDENTIALS_PATH")
        if not self.service_creds_file or not os.path.exists(self.service_creds_file):
            raise FileNotFoundError(f"Service Account credentials file not found at {self.service_creds_file}")
        self.scope = [
            'https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive'
        ]

    def authenticate(self):
        """Authenticate and return a Google API service client."""
        creds = ServiceAccountCredentials.from_json_keyfile_name(self.service_creds_file, self.scope)
        return creds

    def get_gspread_client(self):
        """Create a gspread client for interacting with Google Sheets."""
        creds = self.authenticate()
        client = gspread.authorize(creds)
        return client


def show_sheet_data(gspread_client, sheet_id, sheet_name='Sheet1'):
    """Show data from a specific sheet in Google Sheets."""
    try:
        # Открываем Google Sheet по идентификатору
        sheet = gspread_client.open_by_key(sheet_id)

        # Выбираем лист по имени
        worksheet = sheet.worksheet(sheet_name)

        # Получаем все данные с листа
        data = worksheet.get_all_records()

        # Отображаем данные
        if data:
            for row in data:
                print(row)
        else:
            print("No data found in the sheet.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    # Создаем объект аутентификации
    auth = GoogleServiceAuth()

    # Получаем gspread клиент
    gspread_client = auth.get_gspread_client()

    # Идентификатор таблицы Google Sheets
    sheet_id = '1cWsqTIX1TUR5dQoINP5NhBSV--uHHQaFSbf_RJg5omE'

    # Отображаем данные с листа 'Sheet1'
    show_sheet_data(gspread_client, sheet_id, sheet_name='Sheet1')
