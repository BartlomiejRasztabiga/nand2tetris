import os
import sys
import string
import re


class Parser():
    def parse(self, lines):
        lines = self._clear_lines(lines)
        return list(map(self._parse_line, lines))

    def _parse_line(self, line):
        parsed_line = None

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


class CodeTranslator():
    def convert_instructions(self, instructions):
        converted_instructions = []
        for instruction in instructions:
            converted_instructions.append(self._convert_instruction(instruction))

        return converted_instructions

    def _convert_instruction(self, instruction):
        return []


class VMTranslator():
    def __init__(self):
        self.parser = Parser()
        self.codeTranslator = CodeTranslator()

    def translate(self, lines):
        parsed_instructions = self.parser.parse(lines)
        encoded_instructions = self.codeTranslator.convert_instructions(
            parsed_instructions)

        return list(map(lambda x: x + os.linesep, encoded_instructions))


class Main():
    def __init__(self, in_file, out_file):
        self.in_file = in_file
        self.out_file = out_file

    def run(self):
        # read raw lines
        with open(self.in_file, 'r') as file:
            lines = list(map(lambda x: x.strip(), file.readlines()))

        self.assembler = VMTranslator()
        translated_lines = self.assembler.translate(lines)

        # write translated lines
        with open(self.out_file, 'w') as file:
            file.writelines(translated_lines)


def main():
    if len(sys.argv) < 2:
        print("No input file supplied")
        return

    in_file = sys.argv[1]
    out_file = in_file.replace('.asm', '.hack')

    Main(in_file, out_file).run()


if __name__ == '__main__':
    main()
