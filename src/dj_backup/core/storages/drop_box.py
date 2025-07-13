import warnings
import getpass

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

_oauth_refresh_token = None


class DropBoxConnector(BaseStorageConnector):
    IMPORT_STATUS = package_imported
    CONFIG = {
        'APP_KEY': None,
        'OUT': '/dj_backup/'
    }
    STORAGE_NAME = 'DROPBOX'
    DBX = None

    @classmethod
    def _connect(cls):
        """
            create connection to host server
        """
        c = cls.CONFIG
        dbx = dropbox.Dropbox(oauth2_refresh_token=_oauth_refresh_token, app_key=c['APP_KEY'])
        cls.DBX = dbx
        return dbx

    @classmethod
    def _close(cls):
        """
            close connections
        """
        if cls.DBX: cls.DBX.close()

    def _upload(self, dbx, output):
        with open(self.file_path, 'rb') as file:
            dbx.files_upload(file.read(), output)

    def _save(self):
        self.check_before_save()
        dbx = self.connect()
        file_name = self.get_file_name()
        output = utils.join_paths(self.CONFIG['OUT'], file_name)
        self.upload(dbx, output)
        self.close()

    @classmethod
    def check_before_setup(cls):
        if cls.IMPORT_STATUS is False:
            return False
        return True

    @classmethod
    def setup(cls):
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
