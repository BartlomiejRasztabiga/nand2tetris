import os
import sys
import string
import re


class SymbolTable():
    def __init__(self):
        self.symbols = {
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

    def getSymbolValue(self, symbolName):
        if symbolName not in self.symbols:
            return None
        return self.symbols[symbolName]

    def addSymbol(self, symbolName):
        if symbolName in self.symbols:
            return  # should throw exception
        self.symbols[symbolName] = self.__getNextAvailableValue()

    def addSymbolWithValue(self, symbolName, value):
        if symbolName in self.symbols:
            return  # should throw exception
        if value in self.symbols.values():
            return  # should not happen since line symbols are evaluated first
        self.symbols[symbolName] = value

    def __getNextAvailableValue(self):
        n = 16
        while n in self.symbols.values():
            n += 1
        return n


class Label():
    def __init__(self, label):
        self.label = label

    def __eq__(self, other):
        return self.label == other.label


class AInstruction():
    def __init__(self, address):
        self.address = address

    def __eq__(self, other):
        return self.address == other.address


class CInstruction():
    def __init__(self, comp, dest, jump):
        self.comp = comp
        self.dest = dest
        self.jump = jump

    def __eq__(self, other):
        return self.comp == other.comp and self.dest == other.dest and self.jump == other.jump


class Parser():
    def parse(self, lines):
        lines = self.__clear_lines(lines)
        return list(map(self.__parse_line, lines))

    def __parse_line(self, line):
        parsed_line = None
        if self.__is_label(line):
            parsed_line = Label(line[1:len(line)-1])
        elif self.__is_A_instruction(line):
            parsed_line = AInstruction(line[1:])
        else:
            parsed_line = self.__line_to_C_instruction(line)

        return parsed_line

    def __clear_lines(self, lines):
        return [x for x in map(self.__clear_line, lines) if x is not None]

    def __clear_line(self, line):
        s = "".join(self.__delete_comment(line).split())
        n = len(s)
        return s if n != 0 else None

    def __delete_comment(self, line):
        comment_start_index = line.find('//')
        if comment_start_index == -1:
            return line
        return line[:comment_start_index]

    def __is_label(self, line):
        return re.match(r'\(.*\)', line)

    def __is_A_instruction(self, line):
        return line.startswith('@')

    def __line_to_C_instruction(self, line):
        equal_sign_index = line.find('=')
        semicolon_sign_index = line.find(';')

        dest = None if equal_sign_index == -1 else line[:equal_sign_index]
        jump = None if semicolon_sign_index == - \
            1 else line[semicolon_sign_index + 1:]
        comp = line[0 if equal_sign_index == -1 else equal_sign_index +
                    1: len(line) if semicolon_sign_index == -1 else semicolon_sign_index]

        return CInstruction(comp, dest, jump)


class CodeConverter():
    def convertToBinary(self, line):
        print(type(line))
        return line


class Assembler():
    def __init__(self):
        self.parser = Parser()

    def assemble(self, lines):
        self.parsed_lines = self.parser.parse(lines)
        # print(self.parsed_lines)
        # self.update_symbols()
        return list(map(lambda x: str(x) + os.linesep, self.parsed_lines))

    def __update_symbols(self):
        pass


class Main():
    def __init__(self, in_file, out_file):
        self.in_file = in_file
        self.out_file = out_file

    def run(self):
        # read raw lines
        with open(self.in_file, 'r') as file:
            lines = list(map(lambda x: x.strip(), file.readlines()))

        self.assembler = Assembler()
        assembled_lines = self.assembler.assemble(lines)

        print(assembled_lines)

        # write assembled lines
        with open(self.out_file, 'w') as file:
            file.writelines(assembled_lines)


def main():
    if len(sys.argv) < 2:
        print("No input file supplied")
        return

    in_file = sys.argv[1]
    out_file = in_file.replace('.asm', '.hack')

    Main(in_file, out_file).run()


if __name__ == '__main__':
    main()
