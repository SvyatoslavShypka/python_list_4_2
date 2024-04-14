import sys
import os
import common_tools


class ArgumentCollector:
    def __init__(self):
        self.args = {}

    def add_argument(self, argv):
        for i in range(1, len(argv)):
            if argv[i].startswith("BACKUPS_DIR"):
                self.args["BACKUPS_DIR"] = argv[i][12:]
            else:
                self.args["sciezka"] = argv[i]


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Nie podano folderu")
        sys.exit(1)
    parser = ArgumentCollector()
    parser.add_argument(sys.argv)
    sciezka = parser.args.get("sciezka")
    if not os.path.exists(sciezka):
        print(f"Folder '{sciezka}' nie istnieje.")
        sys.exit(1)

    backup_sciezka = common_tools.tworzymy_backup(sciezka, parser.args.get("BACKUPS_DIR"))
    print(f"Backup stworzono tutaj: {backup_sciezka}")
    # test
    # python backup.py C:\2\projects\Politech3\Python\python_list_4\FOLDER_TO_PACK
    # python backup.py C:\2\projects\Politech3\Python\python_list_4\FOLDER_TO_PACK BACKUPS_DIR=C:\2\projects\Politech3\Python\python_list_4
    #
    # ---set ENV---
    # SET BACKUPS_DIR=C:\2\projects\Politech3\Python\python_list_4\TEST
    # ---check ENV---
    # echo %BACKUPS_DIR%
    # python backup.py C:\2\projects\Politech3\Python\python_list_4\FOLDER_TO_PACK
    # ---remove ENV---
    # SET BACKUPS_DIR=