import sys
from os import environ
from pathlib import Path


def print_path(callback, needed_files):
    # set_extention = {""}
    list_paths = []
    folder_list = environ["PATH"].split(";")
    # W razie systemu Linux
    if len(folder_list) == 1:
        folder_list = environ["PATH"].split(":")
    for folder in folder_list:
        if folder != "":
            path = Path(folder)
            if path.exists():
                list_paths.append(path)
            else:
                print("Ten folder nie istnieje: ", folder)
    # print("-----------------------------------------------")
    for path in sorted(list_paths):
        print(path)
        if needed_files:
            for p in path.iterdir():
                # Sprawdzamy czy jest to plik i czy jest wykonywalny
                if p.is_file() and p.stat().st_mode & 0o111:
                    # To plik, wywołujemy callback
                    callback(p)
                    # set_extention.add(p.suffix)

    # print(set_extention)


def visitfile(file):
    print('W folderze jest wykonywalny plik: ', file.name)


if __name__ == "__main__":
    needed_files = False
    if len(sys.argv) > 1:
        if sys.argv[1].lower() == "files":
            needed_files = True
    # testowy wydruk     python lab_4_2.py
    # testowy wydruk     python lab_4_2.py files
    print_path(visitfile, needed_files)
