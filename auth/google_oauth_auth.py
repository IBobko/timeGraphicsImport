import os

from dotenv import load_dotenv
from google_auth_oauthlib.flow import InstalledAppFlow

from .base_auth import BaseAuth


class GoogleOAuthAuth(BaseAuth):
    def __init__(self):
        super().__init__()  # Call the constructor of BaseAuth
        load_dotenv()
        self.scopes = [
            'https://www.googleapis.com/auth/drive',
            'https://www.googleapis.com/auth/spreadsheets'
        ]
        self.client_secrets_file = os.getenv("GOOGLE_OAUTH_CREDENTIALS_PATH")

        if not self.client_secrets_file:
            raise ValueError(
                "The path to the client secrets file must be set in the GOOGLE_OAUTH_CREDENTIALS_PATH environment variable.")

    def perform_authentication(self):
        """Specific authentication logic for Google OAuth."""
        flow = InstalledAppFlow.from_client_secrets_file(self.client_secrets_file, self.scopes)
        self._credentials = flow.run_local_server(port=0)  # Store credentials in the instance variable
        return self._credentials
