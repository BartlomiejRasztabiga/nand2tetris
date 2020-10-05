import os
import sys
import string
import re


class ArithmeticCommand():
    def __init__(self, command_type):
        self.command_type = command_type

    def to_assembly(self):
        lines = []

        if self.command_type == 'add':
            lines.append('@SP')
            lines.append('AM=M-1')
            lines.append('D=M')
            lines.append('@SP')
            lines.append('AM=M-1')
            lines.append('A=M')
            lines.append('D=A+D')
            lines.append('@SP')
            lines.append('A=M')
            lines.append('M=D')
            lines.append('@SP')
            lines.append('M=M+1')

        # https://github.com/SeaRbSg/nand2tetris/blob/master/stim371/07/vm_code_writer.rb

        return lines


class PushCommand():
    def __init__(self, segment, index):
        self.segment = segment
        self.index = index

    def to_assembly(self):
        lines = []
        if self.segment == 'constant':
            # get constant to D register
            lines.append('@' + self.index)
            lines.append('D=A')

        # push value to stack
        lines.append('@SP')
        lines.append('A=M')
        lines.append('M=D')

        # increment stack pointer
        lines.append('@SP')
        lines.append('M=M+1')

        return lines


class PopCommand():
    def __init__(self, segment, index):
        self.segment = segment
        self.index = index


class LabelCommand():
    def __init__(self, label):
        self.label = label


class GoToCommand():
    def __init__(self):
        pass


class IfCommand():
    def __init__(self):
        pass


class FunctionCommand():
    def __init__(self):
        pass


class ReturnCommand():
    def __init__(self):
        pass


class CallCommand():
    def __init__(self):
        pass


class Parser():
    def parse(self, lines):
        lines = self._clear_lines(lines)
        return list(map(self._parse_line, lines))

    def _parse_line(self, line):
        parsed_line = None

        components = line.split()
        cmd = components[0]
        arg1 = components[1]
        arg2 = components[2]

        if cmd == 'push':
            parsed_line = PushCommand(arg1, arg2)
        elif cmd in ['add', 'sub', 'neg', 'eq', 'gt', 'lt', 'and', 'or', 'not']:
            parsed_line = ArithmeticCommand(cmd)
        elif cmd == 'pop':
            parsed_line = PopCommand(arg1, arg2)
        elif cmd == 'label':
            parsed_line = LabelCommand(arg1)
        elif cmd == 'goto':
            parsed_line = GoToCommand()
        elif cmd == 'if-goto':
            parsed_line = IfCommand()

        return parsed_line

    def _clear_lines(self, lines):
        return [x for x in map(self._clear_line, lines) if x is not None]

    def _clear_line(self, line):
        s = self._delete_comment(line)
        n = len(s)
        return s if n != 0 else None

    def _delete_comment(self, line):
        comment_start_index = line.find('//')
        if comment_start_index == -1:
            return line
        return line[:comment_start_index]


class CodeTranslator():
    def translate(self, instructions):
        translated_instructions = []
        for instruction in instructions:
            translated_instructions += self._translate_instruction(instruction)

        return translated_instructions

    def _translate_instruction(self, instruction):
        return instruction.to_assembly() if instruction is not None else []


class VMTranslator():
    def __init__(self):
        self.parser = Parser()
        self.codeTranslator = CodeTranslator()

    def translate(self, lines):
        instructions = self.parser.parse(lines)

        print(instructions)
        translated_instructions = self.codeTranslator.translate(instructions)

        return list(map(lambda x: x + os.linesep, translated_instructions))


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
    out_file = in_file.replace('.vm', '.asm')

    Main(in_file, out_file).run()


if __name__ == '__main__':
    main()
