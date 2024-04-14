import sys
import string
from collections import Counter


def statystyka(file):
    if file:
        try:
            with open(file, 'r', encoding='utf-8') as f:
                calyText = file.read()
                znaki = len(calyText)
                slowa = len(calyText.split())
                linie = calyText.count('\n')

                byteListLine = f.readlines()
                decoded = []
                for line in byteListLine:
                    # dekodujemy z bajtów w string
                    decoded.append(line.decode("utf-8"))
                lines_to_print = decoded
        except FileNotFoundError:
            print("Nie ma takiego pliku: ", file)
            sys.exit(1)
    else:
        lines_to_print = sys.stdin.readlines()
        lines_all = "\r".join(lines_to_print)
    for line in lines_to_print:
        sys.stdout.buffer.write(line.encode())


class ArgumentCollector:
    def __init__(self):
        self.args = {}

    def add_argument(self, argv):
        for i in range(1, len(argv)):
            if argv[i] != "<" and argv[i] != "type":
                self.args["file"] = argv[i]


if __name__ == "__main__":
    # if len(sys.argv) <= 1:
    #     print("Nie zadano ścieżki do pliku")
    #     sys.exit(1)
    parser = ArgumentCollector()
    parser.add_argument(sys.argv)
    statystyka(parser.args.get("file"))
    # test
    # type sciezka.txt | python lab_4_4plik.py
    # python lab_4_4plik.py sciezka.txt
