import os
import zipfile
import csv
from datetime import datetime


def tworzymy_backup(directory, backup_dir=None):
    if backup_dir is None:
        # Jeżeli w ENV jest zmienna BACKUPS_DIR używamy, inaczej C:\Users\<User>.backups
        backup_dir = os.getenv('BACKUPS_DIR', os.path.join(os.path.expanduser('~'), '.backups'))
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)

    # Nazwa pliku zip na podstawie timestamp
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    backup_file = f"{timestamp}-{os.path.basename(directory)}.zip"
    backup_path = os.path.join(backup_dir, backup_file)

    # Tworzymy ZIP
    with zipfile.ZipFile(backup_path, 'w') as zipf:
        for root, dirs, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, directory))

    # Update CSV z historią kopii zapasowych
    history_file = os.path.join(backup_dir, 'backup_history.csv')
    header = ['Timestamp', 'Directory', 'Backup File']
    record = [timestamp, os.path.abspath(directory), backup_file]
    if not os.path.exists(history_file):
        with open(history_file, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(header)
            writer.writerow(record)
    else:
        with open(history_file, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(record)

    return backup_path


def list_backups(backup_dir=None):
    if backup_dir is None:
        backup_dir = os.getenv('BACKUPS_DIR', os.path.join(os.path.expanduser('~'), '.backups'))
    history_file = os.path.join(backup_dir, 'backup_history.csv')

    backups = []
    if not os.path.exists(history_file):
        return backups

    with open(history_file, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Ignorujemy wiersz-tytuł
        for row in reader:
            backups.append(row)
    return backups, backup_dir
