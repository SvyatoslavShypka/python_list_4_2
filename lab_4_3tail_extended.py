import sys
import time


def tail(file, lines=None, bytes=None, follow=False):
    if bytes is None and lines is None:
        lines = 10

    def read_file(start_pos):
        try:
            with open(file, 'rb') as f:
                f.seek(start_pos)
                byte_list_lines = f.readlines()
                decoded = []
                for line in byte_list_lines:
                    decoded.append(line.decode("utf-8"))
                return decoded, f.tell()  # zwracamy lines_to_print i ostatnią pozycje w pliku
        except FileNotFoundError:
            print("File not found:", file)
            sys.exit(1)

    def print_new_lines(start_pos):
        # ciągle sprawdzamy od ostatnie pozycji
        while True:
            lines_to_print, new_pos = read_file(start_pos)
            for line in lines_to_print:
                sys.stdout.buffer.write(line.encode())
            # nowa pozycja w pliku
            start_pos = new_pos
            time.sleep(1)  # czekamy 1 sekunde i sprawdzamy plik ponownie

    if follow:
        start_pos = 0
        if bytes is not None:
            # Od końca pliku szukamy pozycję dla odczytania pliku
            with open(file, 'rb') as f:
                f.seek(-bytes, 2)
                start_pos = f.tell()
        print_new_lines(start_pos)
    else:
        lines_to_print, _ = read_file(0)
        for line in lines_to_print:
            sys.stdout.buffer.write(line.encode())


class SimpleArgumentParser:
    def __init__(self):
        self.args = {}

    def add_argument(self, argv):
        for i in range(1, len(argv)):
            if argv[i] != "<" and argv[i] != "type":
                if argv[i].startswith("--lines"):
                    self.args["lines"] = int(argv[i][8:])
                elif argv[i].startswith("--bytes"):
                    self.args["bytes"] = int(argv[i][8:])
                elif argv[i] == "--follow":
                    self.args["follow"] = True
                else:
                    self.args["file"] = argv[i]


if __name__ == "__main__":
    parser = SimpleArgumentParser()
    parser.add_argument(sys.argv)
    tail(parser.args.get("file"), parser.args.get("lines"), parser.args.get("bytes"), parser.args.get("follow"))
