import sys


def tail(file, lines=None, bytes=None):
    if bytes is None and lines is None:
        lines = 10

    if file:
        try:
            with open(file, 'rb') as f:
                if bytes is not None:
                    f.seek(-int(bytes), 2)
                byteListLine = f.readlines()
                if lines is not None and lines < len(byteListLine):
                    byteListLine = byteListLine[-int(lines):]
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
        if bytes is not None:
            lines_all = "\r".join(lines_to_print)
            lines_to_print = lines_all[-bytes:]
    if lines is not None and lines < len(lines_to_print):
        # jeżeli lines=0  - nic nie drukujemy
        if lines == 0:
            lines_to_print.clear()
        else:
            # drukujemy tylko parę ostatnich linii
            lines_to_print = lines_to_print[-int(lines):]

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
    if len(sys.argv) <= 1:
        print("Nie zadano ścieżki do pliku")
        sys.exit(1)
    parser = ArgumentCollector()
    parser.add_argument(sys.argv)
    tail(parser.args.get("file"))
    # test
    # type test.txt | python lab_4_3tail.py --bytes=20
    # python lab_4_3tail.py test.txt --bytes=20
    # python lab_4_3tail.py test.txt --lines=15
    # python lab_4_3tail.py test.txt --lines=2
    # python lab_4_3tail.py test.txt --lines=0
    # type test.txt | python lab_4_3tail.py --lines=2
