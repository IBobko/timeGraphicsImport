import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
from dotenv import load_dotenv


class GoogleDriveHandler:
    def __init__(self):
        load_dotenv()
        self.CLIENT_SECRETS_FILE = os.getenv("GOOGLE_API_CREDENTIALS_PATH")
        self.SCOPES = [
            'https://www.googleapis.com/auth/drive'
        ]
        self.service = self._authenticate()

    def _authenticate(self):
        """Authenticate and create the Google Drive API service object."""
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            self.CLIENT_SECRETS_FILE, self.SCOPES)
        credentials = flow.run_local_server(port=0)
        return googleapiclient.discovery.build('drive', 'v3', credentials=credentials)

    def get_folder_id(self, folder_name):
        """Get the folder ID by its name."""
        query = f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder'"
        results = self.service.files().list(q=query, fields="files(id, name)").execute()
        items = results.get('files', [])
        if not items:
            print(f'No folder named "{folder_name}" found.')
            return None
        return items[0]['id']

    def list_files_in_folder(self, folder_name):
        """List all files in a specific Google Drive folder by folder name."""
        folder_id = self.get_folder_id(folder_name)
        if not folder_id:
            return

        query = f"'{folder_id}' in parents"
        results = self.service.files().list(
            q=query,
            pageSize=10,  # Adjust the size to list more or fewer files
            fields="nextPageToken, files(id, name)"
        ).execute()

        items = results.get('files', [])
        if not items:
            print(f'No files found in folder "{folder_name}".')
        else:
            print(f'Files in folder "{folder_name}":')
            for item in items:
                print(f"{item['name']} (ID: {item['id']})")

    def download_file(self, file_id, destination):
        """Download a file from Google Drive."""
        request = self.service.files().get_media(fileId=file_id)
        with open(destination, 'wb') as f:
            downloader = googleapiclient.http.MediaIoBaseDownload(f, request)
            done = False
            while not done:
                status, done = downloader.next_chunk()
                print(f"Download {int(status.progress() * 100)}%.")


# Usage example
if __name__ == "__main__":
    drive_handler = GoogleDriveHandler()

    # List files in the "Time.Graphics" folder on Google Drive
    drive_handler.list_files_in_folder("Time.Graphics")

    # Download a specific file (replace with actual file ID and destination)
    # file_id = 'your-file-id'
    # destination = 'path/to/destination.xlsx'
    # drive_handler.download_file(file_id, destination)
