import sys
import os
import common_tools

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Nie podano folderu")
        sys.exit(1)

    directory = sys.argv[1]
    if not os.path.exists(directory):
        print(f"Folder '{directory}' nie istnieje.")
        sys.exit(1)

    backup_sciezka = common_tools.tworzymy_backup(directory)
    print(f"Backup stworzono tutaj: {backup_sciezka}")
    # test
    # python backup.py C:\2\projects\Politech3\Python\python_list_4\FOLDER_TO_PACK