from office365_api import SharePoint
import sys

SharePoint = SharePoint()

def print_help():
    print('\nHELP FOR UPLOAD FILE\n')
    print('> python upload.py "<path_to_file>" "<sharepoint_folder>"\n')
    print('> Default <sharepoint_folder>: `sharepoint_doc_library` from .env config file.')
    print('> For specific folder of SP site use relative path without root folder.')
    print('> Example: "Sales/Orders" mean path "<site>/Root Folder/Sales/Orders"\n')
    print('> For upload to root folder don\'t specify any path.\n')
    print('> example for Windows: python upload.py "C:\\users\\User Profile\\Documents\\file.pdf" "Sales/Orders"')
    print('> example for Linux: python upload.py "/home/user/Documents/file.pdf" "Sales/Orders"')
    print('\nDon\'t use backslash "\\" in parameters to escape.')

if len(sys.argv) < 2 or sys.argv[1] == 'help':
    print_help()
    exit()

file_dir_path = sys.argv[1]

if file_dir_path.find('\\') == -1:
    split_path = file_dir_path.split('/')
else:
    split_path = file_dir_path.split('\\')

file_name = split_path[-1]

if len(sys.argv) > 2:
    folder = sys.argv[2]
else:
    folder = None

# upload file
SharePoint.upload_file(file_dir_path, file_name, folder)