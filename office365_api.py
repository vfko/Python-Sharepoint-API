import environ
from office365.sharepoint.client_context import ClientContext
from office365.runtime.auth.user_credential import UserCredential
from office365.runtime.auth.client_credential import ClientCredential
from office365.sharepoint.files.file import File
from office365.sharepoint.files.system_object_type import FileSystemObjectType
from shareplum import Site, Office365
from shareplum.site import Version

env = environ.Env()
environ.Env().read_env()

USERNAME = env("sharepoint_email")
PASSWORD = env("sharepoint_password")
SHAREPOINT_URL = env("sharepoint_url")
SHAREPOINT_SITE = env("sharepoint_url_site")
SHAREPOINT_SITE_NAME = env("sharepoint_site_name")
SHAREPOINT_DOC = env("sharepoint_doc_library")
ROOT_FOLDER=env("ROOT_FOLDER")

class SharePoint:

    def __init__(self, timeout=None):
        self.timeout = timeout

    def _auth(self, operation):
        if operation == "download" or operation == "list":
            conn = ClientContext(SHAREPOINT_SITE).with_credentials(
                UserCredential(
                    USERNAME,
                    PASSWORD
                )
            )
            return conn
        elif operation == "upload" or operation == "delete":
            self.authcookie = Office365(SHAREPOINT_URL, username=USERNAME, password=PASSWORD).GetCookies()
            self.site = Site(SHAREPOINT_SITE, version=Version.v365, authcookie=self.authcookie, timeout=None)
            return self.site



    ############
    # Download #
    ############

    def _get_files_list(self, folder_name):
        conn = self._auth("download")
        if folder_name == ROOT_FOLDER:
            target_folder_url = f'{SHAREPOINT_DOC}'
        else:
            target_folder_url = f'{SHAREPOINT_DOC}/{folder_name}'
        root_folder = conn.web.get_folder_by_server_relative_url(target_folder_url)
        root_folder.expand(["Files", "Folders"]).get().execute_query()
        return root_folder.files

    def download_file(self, file_name, folder_name):
        conn = self._auth("download")

        if folder_name != ROOT_FOLDER:
            file_url = f'/sites/{SHAREPOINT_SITE_NAME}/{SHAREPOINT_DOC}/{folder_name}/{file_name}'
        else:
            file_url = f'/sites/{SHAREPOINT_SITE_NAME}/{SHAREPOINT_DOC}/{file_name}'

        file = File.open_binary(conn, file_url)
        return file.content

    def download_files(self, folder_name):
        if folder_name == ROOT_FOLDER:
            folder_name = ""
        return self._get_files_list(folder_name)

    ##########
    # Upload #
    ##########

    def upload_file(self, file_dir_path, file_name, folder):
        site = self._auth("upload")

        if folder != None:
            folder = site.Folder(SHAREPOINT_DOC+folder)
        else:
            folder = site.Folder(SHAREPOINT_DOC)

        with open(file_dir_path, mode='rb') as file:
            fileContent = file.read()

        folder.upload_file(fileContent, file_name)


    ##########
    # Delete #
    ##########

    def delete_file(self, file_name, folder):
        site = self._auth("delete")

        if folder != None:
            folder = site.Folder(SHAREPOINT_DOC+folder)
        else:
            folder = site.Folder(SHAREPOINT_DOC)

        folder.delete_file(file_name)

    ########
    # List #
    ########

    def get_list(self, folder_name):
        conn = self._auth("list")
        list_source = conn.web.get_folder_by_server_relative_url(f'/sites/{SHAREPOINT_SITE_NAME}/{SHAREPOINT_DOC}{folder_name}')
        files = list_source.files
        conn.load(files)
        conn.execute_query()
        arr_of_files = []

        for i in files:
            arr_of_files.append("Folder name: {0}".format(i.properties["ServerRelativeUrl"]))
        
        return arr_of_files
    
    def list_files_with_relative_path(self, folder_name):
        return self.get_list(folder_name)
    
    def list_files(self, folder_name):
        files_with_path = self.get_list(folder_name)
        files = []

        for file in files_with_path:
            split_path = file.split("/")
            files.append(split_path[-1])

        return files