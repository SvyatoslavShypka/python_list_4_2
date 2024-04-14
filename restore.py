import sys
import os
import shutil
import common_tools
import zipfile


def restore_backup(backup_file, restore_dir):
    backup_dir = os.getenv('BACKUPS_DIR', os.path.join(os.path.expanduser('~'), '.backups'))
    backup_path = os.path.join(backup_dir, backup_file)

    if not os.path.exists(backup_path):
        print(f"Backup file '{backup_file}' not found.")
        sys.exit(1)

    if not os.path.exists(restore_dir):
        os.makedirs(restore_dir)
    else:
        # Usuwamy zawartość katalogu, jeżeli istnieje
        for root, dirs, files in os.walk(restore_dir):
            for file in files:
                os.remove(os.path.join(root, file))
            for dir in dirs:
                shutil.rmtree(os.path.join(root, dir))

    with zipfile.ZipFile(backup_path, 'r') as zip_ref:
        zip_ref.extractall(restore_dir)

    print(f"Backup '{backup_file}' restored successfully to '{restore_dir}'.")


class ArgumentCollector:
    def __init__(self):
        self.args = {}

    def add_argument(self, argv):
        for i in range(1, len(argv)):
            if argv[i].startswith("BACKUPS_DIR"):
                self.args["BACKUPS_DIR"] = argv[i][12:]
            else:
                self.args["RESTORE_DIR"] = argv[i]


def main():
    parser = ArgumentCollector()
    parser.add_argument(sys.argv)
    if parser.args.get("RESTORE_DIR"):
        restore_dir = parser.args.get("RESTORE_DIR")
    else:
        # obecny folder
        restore_dir = os.getcwd()
    backups, backup_dir = common_tools.list_backups(parser.args.get("BACKUPS_DIR"))
    if not backups:
        print("Ni odnaleziono backups")
        sys.exit(0)

    print("Available backups:")
    for i, backup in enumerate(backups, start=1):
        print(f"{i}. {backup[0]} - {backup[1]} - {backup[2]}")
    while True:
        choice = input("Wybierz numer backup'u: ")
        try:
            choice = int(choice)
            if choice < 1 or choice > len(backups):
                raise ValueError
            else:
                break
        except ValueError:
            print("Invalid choice.")
    backup_file = os.path.join(backup_dir, backups[choice - 1][2])
    restore_backup(backup_file, restore_dir)


if __name__ == "__main__":
    main()
    # test
    # python restore.py C:\2\projects\Politech3\Python\python_list_4\FOLDER_TO_PACK
    # python restore.py C:\2\projects\Politech3\Python\python_list_4\FOLDER_TO_PACK BACKUPS_DIR=C:\2\projects\Politech3\Python\python_list_4\TEST
