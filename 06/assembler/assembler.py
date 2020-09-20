import string

symbols = {
    'R0': 0,
    'R1': 1,
    'R2': 2,
    'R3': 3,
    'R4': 4,
    'R5': 5,
    'R6': 6,
    'R7': 7,
    'R8': 8,
    'R9': 9,
    'R10': 10,
    'R11': 11,
    'R12': 12,
    'R13': 13,
    'R14': 14,
    'R15': 15,
    'SCREEN': 16384,
    'KBD': 24576,
    'SP': 0,
    'LCL': 1,
    'ARG': 2,
    'THIS': 3,
    'THAT': 4
}


class Parser():
    def parse(self, lines):
        parsed = []
        lines = self.clear_lines(lines)

        print(lines)

        return lines

    def clear_lines(self, lines):
        return [x for x in map(self.clear_line, lines) if x is not None]

    def clear_line(self, line):
        s = "".join(self.delete_comment(line).split())
        n = len(s)
        return s if n != 0 else None

    def delete_comment(self, line):
        comment_start_index = line.find('//')
        if comment_start_index == -1:
            return line
        return line[:comment_start_index]

    def is_label(self, line):
        pass


def update_symbols(parser, lines):
    parser.parse(lines)


def main():
    in_file = 'in.asm'
    out_file = 'out.hack'
    parser = Parser()

    with open(in_file, 'r') as file:
        lines = list(map(lambda x: x.strip(), file.readlines()))
        update_symbols(parser, lines)


if __name__ == '__main__':
    main()
