import warnings
import getpass

from typing import Optional, Union

from pathlib import Path

try:
    import dropbox

    package_imported = True
except ImportError:
    package_imported = False
    warnings.warn("""
        To use the storage provider 'Dropbox', you need to install its package; otherwise, it cannot be used.
        You can install the required package using the following command:
        'pip install djbackup[dropbox]'""")

from dj_backup.core import utils
from .base import BaseStorageConnector

_oauth_refresh_token: Optional[str] = None


class DropBoxConnector(BaseStorageConnector):
    """
    A connector class for interacting with Dropbox storage.

    This class provides methods to connect to Dropbox, upload files, and manage
    the OAuth2 authentication process.

    Attributes:
        IMPORT_STATUS (bool): Indicates whether the Dropbox package was imported successfully.
        CONFIG (dict): Configuration settings for Dropbox integration.
        STORAGE_NAME (str): Name of the storage provider.
        DBX (dropbox.Dropbox): The Dropbox connection object.
    """

    IMPORT_STATUS: bool = package_imported
    CONFIG: dict = {
        'APP_KEY': None,
        'OUT': '/dj_backup/'
    }
    STORAGE_NAME = 'DROPBOX'
    DBX: Optional[dropbox.Dropbox] = None

    @classmethod
    def _connect(cls) -> dropbox.Dropbox:
        """
            Create a connection to the Dropbox server.

            :return: An instance of the Dropbox connection.
        """
        c = cls.CONFIG
        dbx = dropbox.Dropbox(oauth2_refresh_token=_oauth_refresh_token, app_key=c['APP_KEY'])
        cls.DBX = dbx
        return dbx

    @classmethod
    def _close(cls) -> None:
        """
            Close the Dropbox connection.

            This method ensures that any open connections to Dropbox are properly closed.
        """
        if cls.DBX:
            cls.DBX.close()

    def _upload(self, dbx: dropbox.Dropbox, output: Union[str, Path]) -> None:
        """
            Upload a file to Dropbox.

            :param dbx: The Dropbox connection object.
            :param output: The destination path in Dropbox where the file will be uploaded.
        """
        with open(self.file_path, 'rb') as file:
            dbx.files_upload(file.read(), output)

    def _save(self) -> None:
        """
            Save the file to Dropbox after performing necessary checks.

            This method checks conditions before saving, establishes a connection,
            uploads the file, and then closes the connection.
        """
        self.check_before_save()
        dbx = self.connect()
        file_name = self.get_file_name()
        output = utils.join_paths(self.CONFIG['OUT'], file_name)
        self.upload(dbx, output)
        self.close()

    @classmethod
    def check_before_setup(cls) -> bool:
        """
            Check prerequisites before setting up Dropbox access.

            :return: True if setup can proceed, False otherwise.
        """
        return cls.IMPORT_STATUS

    @classmethod
    def setup(cls) -> None:
        """
            Set up Dropbox access using OAuth2.

            This method initiates the OAuth2 flow to obtain an authorization code
            and refresh token for accessing Dropbox.
        """
        if not cls.check_before_setup():
            return

        global _oauth_refresh_token
        c = cls.CONFIG
        auth_flow = dropbox.DropboxOAuth2FlowNoRedirect(c['APP_KEY'], use_pkce=True, token_access_type='offline')

        authorize_url = auth_flow.start()

        W_BOLD = "\033[1;37m"
        BLUE_BOLD = "\033[1;34m"
        G_BOLD = "\033[1;32m"
        RESET = "\033[0m"

        print(f"{BLUE_BOLD}--- Setup DropBox Access(OAUTH) Started ! ---{RESET}")
        print(f"{W_BOLD}1. Go to: {authorize_url}{RESET}")
        print(f"{W_BOLD}2. Click \"Allow\" (you might have to log in first).{RESET}")
        print(f"{W_BOLD}3. Copy the authorization code.{RESET}")

        try:
            auth_code = getpass.getpass(f"{W_BOLD}Enter the authorization code here: {RESET}").strip()
        except KeyboardInterrupt:
            raise KeyboardInterrupt('Setup dropbox access failed [You must enter authorization code]')

        oauth_result = auth_flow.finish(auth_code)

        _oauth_refresh_token = oauth_result.refresh_token

        print(f"{G_BOLD}--- Setup DropBox Access(OAUTH) Finished Successfully ! ---{RESET}")
