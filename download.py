from office365_api import SharePoint
import re
import sys, os
import environ
from pathlib import PurePath

env = environ.Env()
environ.Env().read_env()
ROOT_FOLDER = env('ROOT_FOLDER')

def print_help():
    print('\nHELP FOR DOWNLOAD FILE\n')
    print('> python download.py "<path_to_local_file>" <sharepoint_path> <other_option>\n')
    print('<path_to_local_folder> = path to folder for downloaded files')
    print('\n<sharepoint_path> = path to folder in SharePoint. (default = root)')
    print(f'<sharepoint_path> example1: "{ROOT_FOLDER}" -> <site>/Root Folder/')
    print('<sharepoint_path> example2: "Sales/Orders" -> <site>/Root Folder/Sales/Orders')
    print('\n<other_option>:')
    print('--by-name <name_of_file> = download 1 file with specific name')
    print('--by-pattern <part_of_file_name> = download all files contains this value')
    print('\nExample: download.py "C:\\Users\\User Profile\\Downloads" => download all files from <site>/Root Folder/ to this local folder.')
    print('\nExample: download.py "C:\\Users\\User Profile\\Downloads" Sales/Orders --by-name "file.pdf" => download <site>/Root Folder/Sales/Orders/file.pdf')
    print(f'\nExample: download.py "C:\\Users\\User Profile\\Downloads" {ROOT_FOLDER} --by-pattern "pattern-word" => download all files from <site>/Root Folder/ what contain "pattern-word"')


if len(sys.argv) < 2:
    print('Missing parameter.')
    print('Use `download.py help` for more information.')
    exit()
elif len(sys.argv) > 1:
    if sys.argv[1] == "help":
        print_help()
        exit()
    else:
        FOLDER_DEST = sys.argv[1]

# Sharepoint folder name. May include subfolders YouTube/2022
FOLDER_NAME = ""
try:
    if sys.argv[2].lower() == ROOT_FOLDER:
        FOLDER_NAME == ROOT_FOLDER
    FOLDER_NAME = sys.argv[2]
except:
    FOLDER_NAME = ROOT_FOLDER

# SharePoint file name or file pattern
try:
    options = ["--by-name", "--by-pattern"]
    if sys.argv[3] == options[0]:
        try:
            FILE_NAME = sys.argv[4]
            FILE_NAME_PATTERN = None
        except:
            print(f'Missing {options[0]} value.')
            print("Try `download.py help` for more information.")
            os._exit(1)
    elif sys.argv[3] == options[1]:
        try:
            FILE_NAME_PATTERN = sys.argv[4]
            FILE_NAME = None
        except:
            print(f'Missing {options[1]} value.')
            print("Try `download.py help` for more information.")
            os._exit(1)
    elif sys.argv[2] == options[0] or sys.argv[2] == options[1]:
        print(f'\n\nMissing SharePoint path. Specify SP folder or use "{ROOT_FOLDER}" for Root Folder.')
        print('For more information use `download.py help`.\n\n')
        print(f'\nExample: download.py {sys.argv[1]} "{ROOT_FOLDER}" {sys.argv[2]} ...')
        os._exit(1)
except:
    FILE_NAME = None
    FILE_NAME_PATTERN = None


# Download files
def save_file(file_n, file_obj):
    file_dir_path = PurePath(FOLDER_DEST, file_n)
    with open(file_dir_path, 'wb') as f:
        f.write(file_obj)

def get_file(file_n, folder):
    file_obj = SharePoint().download_file(file_n, folder)
    save_file(file_n, file_obj)

def get_files(folder):
    files_list = SharePoint().download_files(folder)
    for file in files_list:
        get_file(file.name, folder)

def get_files_by_pattern(keyword, folder):
    files_list = SharePoint()._get_files_list(folder)
    for file in files_list:
        if re.search(keyword, file.name):
            get_file(file.name, folder)

if __name__ == '__main__':
    if FILE_NAME != None:
        get_file(FILE_NAME, FOLDER_NAME)
    elif FILE_NAME_PATTERN != None:
        get_files_by_pattern(FILE_NAME_PATTERN, FOLDER_NAME)
    else:
        get_files(FOLDER_NAME)