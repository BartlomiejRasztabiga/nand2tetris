import unittest
from assembler import SymbolTable, Parser, AInstruction, CInstruction, Label, Assembler, CodeConverter


class TestSymbolTable(unittest.TestCase):

    def test_get_builtin_symbol(self):
        symbolTable = SymbolTable()

        self.assertEqual(symbolTable.get_symbol_value('R0'), 0)

    def test_not_existing_symbol(self):
        symbolTable = SymbolTable()

        self.assertEqual(symbolTable.get_symbol_value('none'), None)

    def test_add_new_symbols(self):
        symbolTable = SymbolTable()
        symbolTable.add_symbol('first')
        symbolTable.add_symbol('second')

        self.assertEqual(symbolTable.get_symbol_value('first'), 16)
        self.assertEqual(symbolTable.get_symbol_value('second'), 17)

    def test_add_new_symbols_with_values(self):
        symbolTable = SymbolTable()
        symbolTable.add_symbol_with_value('first', 16)
        symbolTable.add_symbol_with_value('second', 17)

        self.assertEqual(symbolTable.get_symbol_value('first'), 16)
        self.assertEqual(symbolTable.get_symbol_value('second'), 17)

    def test_symbols_collisions(self):
        symbolTable = SymbolTable()
        symbolTable.add_symbol_with_value('first', 16)
        symbolTable.add_symbol_with_value('second', 17)
        symbolTable.add_symbol('third')

        self.assertEqual(symbolTable.get_symbol_value('first'), 16)
        self.assertEqual(symbolTable.get_symbol_value('second'), 17)
        self.assertEqual(symbolTable.get_symbol_value('third'), 18)


class TestParser(unittest.TestCase):
    def test_parse_lines_a_instruction1(self):
        parser = Parser()
        lines_to_parse = ['@R0']

        parsed_lines = parser.parse(lines_to_parse)

        self.assertEqual(parsed_lines, [AInstruction('R0')])

    def test_parse_lines_a_instruction2(self):
        parser = Parser()
        lines_to_parse = ['@2']

        parsed_lines = parser.parse(lines_to_parse)

        self.assertEqual(parsed_lines, [AInstruction('2')])

    def test_parse_lines_c_instruction1(self):
        parser = Parser()
        lines_to_parse = ['D=M']

        parsed_lines = parser.parse(lines_to_parse)

        self.assertEqual(parsed_lines, [CInstruction('M', 'D', None)])

    def test_parse_lines_c_instruction2(self):
        parser = Parser()
        lines_to_parse = ['D;JGT']

        parsed_lines = parser.parse(lines_to_parse)

        self.assertEqual(parsed_lines, [CInstruction('D', None, 'JGT')])

    def test_parse_comment(self):
        parser = Parser()
        lines_to_parse = ['//test']

        parsed_lines = parser.parse(lines_to_parse)

        self.assertEqual(parsed_lines, [])

    def test_parse_label(self):
        parser = Parser()
        lines_to_parse = ['(LABEL)']

        parsed_lines = parser.parse(lines_to_parse)

        self.assertEqual(parsed_lines, [Label('LABEL')])


class TestCodeConverter(unittest.TestCase):
    def test_a_instruction_1(self):
        codeConverter = CodeConverter()

        converted = codeConverter.convert_instructions([AInstruction('2')])

        self.assertEqual(converted, ['0000000000000010'])

    def test_c_instruction_1(self):
        codeConverter = CodeConverter()

        converted = codeConverter.convert_instructions(
            [CInstruction('A', 'D', None)])

        self.assertEqual(converted, ['1110110000010000'])


class TestAssembler(unittest.TestCase):
    def test_assembler1(self):
        assembler = Assembler()

        # assembled = assembler.assemble(['@R0',
        #                                 'D=M              // D = first number',
        #                                 '@R1',
        #                                 'D=D-M            // D = first number - second number',
        #                                 '@OUTPUT_FIRST',
        #                                 'D;JGT            // if D>0 (first is greater) goto output_first',
        #                                 '@R1',
        #                                 'D=M              // D = second number',
        #                                 '@OUTPUT_D',
        #                                 '0;JMP            // goto output_d',
        #                                 '(OUTPUT_FIRST)',
        #                                 '@R0',
        #                                 'D=M              // D = first number',
        #                                 '(OUTPUT_D)',
        #                                 '@R2',
        #                                 'M=D              // M[2] = D (greatest number)',
        #                                 '(INFINITE_LOOP)',
        #                                 '@INFINITE_LOOP',
        #                                 '0;JMP            // infinite loop'])

        # assembled = assembler.assemble(['@R0'])

        # self.assertEqual(assembled, '')


if __name__ == '__main__':
    unittest.main()
