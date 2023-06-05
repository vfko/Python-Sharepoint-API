from office365_api import SharePoint
import sys
import os


SharePoint = SharePoint()
with_path = False
folder_name = ""
options = ["--path", "--to-file", "--append"]
path = False
to_file = False
to_file_value = ""
file_open_option = "w"

# Print help
def print_help():
    print('\n list.py <sharepoint_path> <option>\n')
    print('<sharepoint_path>: optional (default=/Root Folder/)\n')
    print('--path: list files with sharePoint ralative path - optional')
    print('--to-file <path>: save list of files to file - optioal')
    print('--append: write list of files to the end of the file - optional (default=rewrite)\n')
    print('Example1: list.py => print all files from SP "<site>/Root Folder/" to concole')
    print('Example2: list.py --path => list all files with their relative path from SP "<site>/Root Folder/" to console')
    print('Example3: list.py Sales/Orderes --to-file "/path/to/file.txt" --append => write list of SP files from "<site>/Root Folder/Sales/Orderes" to the end of the file')

try:
    if sys.argv[1] == "help":
        print_help()
        os._exit(1)
except Exception:
    pass

# set folder name
def checkIfFolderNameIsMissing():
    if len(sys.argv) > 1:
        for i in options:
            if i == sys.argv[1]:
                return True
    elif len(sys.argv) < 2:
        return True
    
    return False

is_folder_name_missing = checkIfFolderNameIsMissing()
if not is_folder_name_missing and len(sys.argv) > 1:
    folder_name = sys.argv[1]

# set <option> parameters
def checkIfPathExist(path_index):
    try:
        if "--" in sys.argv[path_index]:
            print('The path to the file to save the list is missing.')
            print('--to-path <path_to_file>')
            os._exit(1)
    except:
        print('The path to the file to save the list is missing.')
        print('--to-path <path_to_file>')
        os._exit(1)

for i in range(len(sys.argv)):
    if sys.argv[i] == options[0]:
        path = True
    elif sys.argv[i] == options[1]:
        to_file = True
        path_index = (i+1)
        checkIfPathExist(path_index)
        to_file_value = sys.argv[path_index]
    elif sys.argv[i] == options[2]:
        file_open_option = "a"

# list files
if path == True:
    files_with_path = SharePoint.list_files_with_relative_path(folder_name)
    count_of_files = len(files_with_path)

    if file_open_option == "a":
        new_line = True
    else:
        new_line = False

    for i in files_with_path:
        if to_file == False:
            print(i)
        else:
            f = open(to_file_value, file_open_option)
            if file_open_option == "a" and new_line == True:
                f.write('\n')
                new_line = False
            f.write(f'{i}')
            count_of_files -= 1
            if count_of_files != 0:
                f.write('\n')
            file_open_option = "a"
else:
    files = SharePoint.list_files(folder_name)
    count_of_files = len(files)

    if file_open_option == "a":
        new_line = True
    else:
        new_line = False

    for i in files:
        if to_file == False:
            print(i)
        else:
            f = open(to_file_value, file_open_option)
            if file_open_option == "a" and new_line == True:
                f.write('\n')
                new_line = False
            f.write(f'{i}')
            count_of_files -= 1
            if count_of_files != 0:
                f.write('\n')
            file_open_option = "a"
            file_open_option = "a"