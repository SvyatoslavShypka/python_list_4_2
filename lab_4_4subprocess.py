import os
import subprocess
import sys
from collections import Counter

def run_statystyka(file_path):
    try:
        process = subprocess.Popen(['python', 'lab_4_4plik.py'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
        stdout, _ = process.communicate(input=file_path+'\n')
        return stdout
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")
        sys.exit(1)

def process_output(output):
    lines = output.strip().split('\n')
    stats = {'files': len(lines)}
    total_chars = 0
    total_words = 0
    total_lines = 0
    char_counter = Counter()
    word_counter = Counter()
    for line in lines:
        file_path, chars, words, lines, most_common_char, most_common_word = line.split('\t')
        total_chars += int(chars)
        total_words += int(words)
        total_lines += int(lines)
        char_counter[most_common_char] += 1
        word_counter[most_common_word] += 1
    stats['total_chars'] = total_chars
    stats['total_words'] = total_words
    stats['total_lines'] = total_lines
    stats['most_common_char'] = char_counter.most_common(1)[0][0] if char_counter else None
    stats['most_common_word'] = word_counter.most_common(1)[0][0] if word_counter else None
    return stats

def main(directory):
    file_paths = [os.path.join(directory, file) for file in os.listdir(directory) if os.path.isfile(os.path.join(directory, file))]
    output_list = []
    for file_path in file_paths:
        output = run_statystyka(file_path)
        output_list.append(process_output(output))
    return output_list

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py directory_path")
        sys.exit(1)
    directory = sys.argv[1]
    stats_list = main(directory)
    for stats in stats_list:
        print(stats)
    # test
    # python lab_4_4subprocess.py C:\2\projects\Politech3\Python\python_list_4\TEST
