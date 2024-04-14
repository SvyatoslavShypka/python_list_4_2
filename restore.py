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
        # Usuń zawartość katalogu, jeśli istnieje
        for root, dirs, files in os.walk(restore_dir):
            for file in files:
                os.remove(os.path.join(root, file))
            for dir in dirs:
                shutil.rmtree(os.path.join(root, dir))

    with zipfile.ZipFile(backup_path, 'r') as zip_ref:
        zip_ref.extractall(restore_dir)

    print(f"Backup '{backup_file}' restored successfully to '{restore_dir}'.")


def main():
    restore_dir = os.getcwd() if len(sys.argv) < 2 else sys.argv[1]
    backups = common_tools.list_backups()
    if not backups:
        print("Ni odnaleziono backups")
        sys.exit(0)

    print("Available backups:")
    for i, backup in enumerate(backups, start=1):
        print(f"{i}. {backup[0]} - {backup[1]} - {backup[2]}")

    choice = input("Wybierz numer backup'u: ")
    try:
        choice = int(choice)
        if choice < 1 or choice > len(backups):
            raise ValueError
    except ValueError:
        print("Invalid choice.")
        sys.exit(1)

    backup_file = backups[choice - 1][2]
    restore_backup(backup_file, restore_dir)


if __name__ == "__main__":
    main()
