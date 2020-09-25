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

    def get_symbol_value(self, symbolName):
        if symbolName not in self.symbols:
            return None
        return self.symbols[symbolName]

    def add_symbol(self, symbolName):
        if symbolName in self.symbols:
            return  # should throw exception
        self.symbols[symbolName] = self._get_next_available_value()

    def add_symbol_with_value(self, symbolName, value):
        if symbolName in self.symbols:
            return  # should throw exception
        if value in self.symbols.values():
            return  # should not happen since line symbols are evaluated first
        self.symbols[symbolName] = value

    def _get_next_available_value(self):
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

    def to_binary(self):
        try:
            converted = ('0' + bin(int(self.address))
                         [2:]).rjust(16, '0')
        except ValueError:
            converted = '0000000000000000'
            # should not happen, probably line contains a symbol
        return converted


class CInstruction():
    def __init__(self, comp, dest, jump):
        self.comp = comp
        self.dest = dest
        self.jump = jump

    def __eq__(self, other):
        return self.comp == other.comp and self.dest == other.dest and self.jump == other.jump

    def to_binary(self):
        return '0' * 16


class Parser():
    def parse(self, lines):
        lines = self._clear_lines(lines)
        return list(map(self._parse_line, lines))

    def _parse_line(self, line):
        parsed_line = None
        if self._is_label(line):
            parsed_line = Label(line[1:len(line)-1])
        elif self._is_A_instruction(line):
            parsed_line = AInstruction(line[1:])
        else:
            parsed_line = self._line_to_C_instruction(line)

        return parsed_line

    def _clear_lines(self, lines):
        return [x for x in map(self._clear_line, lines) if x is not None]

    def _clear_line(self, line):
        s = "".join(self._delete_comment(line).split())
        n = len(s)
        return s if n != 0 else None

    def _delete_comment(self, line):
        comment_start_index = line.find('//')
        if comment_start_index == -1:
            return line
        return line[:comment_start_index]

    def _is_label(self, line):
        return re.match(r'\(.*\)', line)

    def _is_A_instruction(self, line):
        return line.startswith('@')

    def _line_to_C_instruction(self, line):
        equal_sign_index = line.find('=')
        semicolon_sign_index = line.find(';')

        dest = None if equal_sign_index == -1 else line[:equal_sign_index]
        jump = None if semicolon_sign_index == - \
            1 else line[semicolon_sign_index + 1:]
        comp = line[0 if equal_sign_index == -1 else equal_sign_index +
                    1: len(line) if semicolon_sign_index == -1 else semicolon_sign_index]

        return CInstruction(comp, dest, jump)


class CodeConverter():
    def convert_instructions(self, instructions):
        return list(map(self._convert_instruction, instructions))

    def _convert_instruction(self, instruction):
        return instruction.to_binary()


class Assembler():
    def __init__(self):
        self.parser = Parser()
        self.codeConverter = CodeConverter()

    def assemble(self, lines):
        self.parsed_instructions = self.parser.parse(lines)
        # print(self.parsed_lines)
        self.__update_symbols()
        self.encoded_instructions = self.codeConverter.convert_instructions(
            self.parsed_instructions)
        # print(self.encoded_lines)

        return list(map(lambda x: x + os.linesep, self.encoded_instructions))

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
