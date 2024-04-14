import os
import subprocess
import sys
from collections import Counter


def subprocess_plik(file_path):
    try:
        process = subprocess.Popen(['python', 'lab_4_4plik.py'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
        stdout, _ = process.communicate(input=file_path+'\n')
        return stdout
    except subprocess.CalledProcessError as e:
        print(f"Błąd w subprocess: {e}")
        sys.exit(1)


def summary(output):
    lines = output.strip().split('\n')
    statistics = {'files': len(lines)}
    znaki = 0
    slowa = 0
    linie = 0
    licznik_znakow = Counter()
    licznik_slow = Counter()
    for line in lines:
        file_path, chars, words, lines, most_common_char, most_common_word = line.split('\t')
        znaki += int(chars)
        slowa += int(words)
        linie += int(lines)
        licznik_znakow[most_common_char] += 1
        licznik_slow[most_common_word] += 1
    statistics['znaki'] = znaki
    statistics['slowa'] = slowa
    statistics['linie'] = linie
    statistics['czestyZnak'] = licznik_znakow.most_common(1)[0][0] if licznik_znakow else None
    statistics['czesteSlowo'] = licznik_slow.most_common(1)[0][0] if licznik_slow else None
    return statistics


def root(directory):
    file_paths = [os.path.join(directory, file) for file in os.listdir(directory) if os.path.isfile(os.path.join(directory, file))]
    result = []
    for file_path in file_paths:
        output = subprocess_plik(file_path)
        result.append(summary(output))
    return result


def sumaryczna_statystyka(statistics_list):
    summary = {
        'files': 0,
        'znaki': 0,
        'slowa': 0,
        'linie': 0,
        'czestyZnak': None,
        'czesteSlowo': None
    }
    licznik_znakow = Counter()
    licznik_slow = Counter()
    for stats in statistics_list:
        summary['files'] += stats['files']
        summary['znaki'] += stats['znaki']
        summary['slowa'] += stats['slowa']
        summary['linie'] += stats['linie']
        licznik_znakow[stats['czestyZnak']] += 1
        licznik_slow[stats['czesteSlowo']] += 1
    # Częsty znak
    if licznik_znakow:
        summary['czestyZnak'] = licznik_znakow.most_common(1)[0][0]
    # Częste słowo
    if licznik_slow:
        summary['czesteSlowo'] = licznik_slow.most_common(1)[0][0]
    return summary


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Nie zadana ścieżka do folderu")
        sys.exit(1)
    folder = sys.argv[1]
    statistics_list = root(folder)
    for statistic in statistics_list:
        print(statistic)
    # Podsumowanie
    summary_stats = sumaryczna_statystyka(statistics_list)
    print("Podsumowanie wszystkich plików:")
    for key, value in summary_stats.items():
        print(f"{key}: {value}")
    # test
    # python lab_4_4subprocess.py C:\2\projects\Politech3\Python\python_list_4\TEST
