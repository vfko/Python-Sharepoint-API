from office365_api import SharePoint
import sys

SharePoint = SharePoint()

if len(sys.argv) < 2:
    print('Missing argument.')
    print('Use `delete.py help` for more information.')

def print_help():
    print('\n delete.py <path_to_file>\n')
    print('Example: delete.py file.pdf => <site>/Root Folder/file.pdf')
    print('Example: delete.py Sales/Orders/file.pdf => <site>/Root Folder/Sales/Orders/file.pdf\n')
    print('If you specify bad file name, you get 404 error.')

if sys.argv[1] != "help":
    file_name = sys.argv[1]
else:
    print_help()
    exit()

# file_name = split_path[-1]

if len(sys.argv) > 2:
    folder = sys.argv[2]
else:
    folder = None

SharePoint.delete_file(file_name, folder)