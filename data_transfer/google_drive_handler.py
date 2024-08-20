import googleapiclient.discovery

from auth.google_service_auth import GoogleServiceAuth


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

    def create_file(self, file_name, mime_type='application/vnd.google-apps.document', folder_name=None):
        """Create a new file in Google Drive."""
        body = {
            'name': file_name,
            'mimeType': mime_type
        }

        # If a folder name is specified, find the folder and set it as the parent
        if folder_name:
            folder_id = self.get_folder_id(folder_name)
            if folder_id:
                body['parents'] = [folder_id]
            else:
                print(f"Folder '{folder_name}' not found. Creating file in root.")

        # Create the file
        try:
            file = self.service.files().create(body=body, fields='id, name').execute()
            print(f"File '{file['name']}' created with ID: {file['id']}")
            return file['id']
        except Exception as e:
            print(f"Failed to create file: {e}")
            return None

    def find_file_by_name(self, file_name, folder_name=None):
        query = f"name = '{file_name}'"
        if folder_name:
            folder_id = self.get_folder_id(folder_name)
            if folder_id:
                query += f" and '{folder_id}' in parents"
        results = self.service.files().list(q=query, fields="files(id, name)").execute()
        files = results.get('files', [])
        if files:
            return files[0]['id']
        return None

    def delete_file(self, file_id):
        """Delete a file from Google Drive by its ID."""
        try:
            self.service.files().delete(fileId=file_id).execute()
            print(f"File with ID: {file_id} has been deleted.")
        except Exception as e:
            print(f"Failed to delete file: {e}")

    def share_file(self, file_id, user_email=None, role='reader', type='user'):
        """Share a Google Drive file with a specific user or make it public."""
        try:
            if user_email:
                permission = {
                    'type': type,
                    'role': role,
                    'emailAddress': user_email
                }
            else:
                # If no user_email is provided, make the file public
                permission = {
                    'type': 'anyone',
                    'role': role
                }

            # Create the permission on the file
            self.service.permissions().create(
                fileId=file_id,
                body=permission,
                fields='id'
            ).execute()
            print(f"File {file_id} shared successfully with {user_email if user_email else 'anyone'}.")
        except Exception as e:
            print(f"Failed to share file: {e}")


# Usage example
if __name__ == "__main__":
    auth = GoogleServiceAuth()
    drive_handler = GoogleDriveHandler(auth)

    # List files in the root directory of Google Drive
    drive_handler.list_root_files()

    # List files in the "Time.Graphics" folder on Google Drive
# drive_handler.list_files_in_folder("Time.Graphics")
