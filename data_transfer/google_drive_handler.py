from auth.google_service_auth import GoogleServiceAuth
import googleapiclient.discovery


class GoogleDriveHandler:
    def __init__(self, auth: GoogleServiceAuth):
        self.service = self._authenticate(auth)

    def _authenticate(self, auth: GoogleServiceAuth):
        """Authenticate and create the Google Drive API service object using provided auth."""
        creds = auth.authenticate()
        return googleapiclient.discovery.build('drive', 'v3', credentials=creds)

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

    def list_root_files(self):
        """List all files and folders in the root of Google Drive."""
        results = self.service.files().list(
            fields="nextPageToken, files(id, name, mimeType)",
            pageSize=100  # You can adjust the size to list more or fewer files
        ).execute()

        items = results.get('files', [])
        if not items:
            print('No files found in the root directory.')
        else:
            print('Files and folders in the root directory:')
            for item in items:
                print(f"{item['name']} (ID: {item['id']}, Type: {item['mimeType']})")

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
    auth = GoogleServiceAuth()
    drive_handler = GoogleDriveHandler(auth)

    # List files in the root directory of Google Drive
    drive_handler.list_root_files()

    # List files in the "Time.Graphics" folder on Google Drive
   # drive_handler.list_files_in_folder("Time.Graphics")
