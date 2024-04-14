import sys
import string
from collections import Counter


def statystyka():
    sciezka = sys.stdin.readline().strip()
    try:
        with open(sciezka, 'r', encoding='utf-8') as f:
            calyText = f.read()
            # print("calyText: ", calyText)
            znaki = len(calyText)
            # print("znaki", znaki)
            slowa = len(calyText.split())
            # print("slowa", slowa)
            linie = calyText.count('\n') + 1 # + ostatnia linia
            # print("linie", linie)
            LicznikZnakow = Counter(calyText)
            # print(LicznikZnakow.items())
            max_wystapien = 0
            czestyZnak = None
            for znak, wystapienia in LicznikZnakow.items():
                if wystapienia > max_wystapien:
                    max_wystapien = wystapienia
                    czestyZnak = znak
            # print("czestyZnak: '", czestyZnak, "' wystapienia", max_wystapien)
            translator = str.maketrans('', '', string.punctuation)
            words = calyText.translate(translator).lower().split()
            word_count = Counter(words)
            max_wystapien_slowo = 0
            czesteSlowo = None
            for slowo, wystapienia in word_count.items():
                if wystapienia > max_wystapien_slowo:
                    max_wystapien_slowo = wystapienia
                    czesteSlowo = slowo
            # print(czesteSlowo)
            # Wyniki jako tsv
            print(f"{sciezka}\t{znaki}\t{slowa}\t{linie}\t{czestyZnak}\t{czesteSlowo}", end="", file=sys.stdout)
    except FileNotFoundError:
        print("Nie ma takiego pliku: ", sciezka)
        sys.exit(1)


if __name__ == "__main__":
    statystyka()
    # test
    # type sciezka.txt | python lab_4_4plik.py
