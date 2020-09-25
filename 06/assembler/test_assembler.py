import unittest
from assembler import SymbolTable, Parser, AInstruction, CInstruction, Label


class TestSymbolTable(unittest.TestCase):

    def test_get_builtin_symbol(self):
        symbolTable = SymbolTable()

        self.assertEqual(symbolTable.getSymbolValue('R0'), 0)

    def test_not_existing_symbol(self):
        symbolTable = SymbolTable()

        self.assertEqual(symbolTable.getSymbolValue('none'), None)

    def test_add_new_symbols(self):
        symbolTable = SymbolTable()
        symbolTable.addSymbol('first')
        symbolTable.addSymbol('second')

        self.assertEqual(symbolTable.getSymbolValue('first'), 16)
        self.assertEqual(symbolTable.getSymbolValue('second'), 17)

    def test_add_new_symbols_with_values(self):
        symbolTable = SymbolTable()
        symbolTable.addSymbolWithValue('first', 16)
        symbolTable.addSymbolWithValue('second', 17)

        self.assertEqual(symbolTable.getSymbolValue('first'), 16)
        self.assertEqual(symbolTable.getSymbolValue('second'), 17)

    def test_symbols_collisions(self):
        symbolTable = SymbolTable()
        symbolTable.addSymbolWithValue('first', 16)
        symbolTable.addSymbolWithValue('second', 17)
        symbolTable.addSymbol('third')

        self.assertEqual(symbolTable.getSymbolValue('first'), 16)
        self.assertEqual(symbolTable.getSymbolValue('second'), 17)
        self.assertEqual(symbolTable.getSymbolValue('third'), 18)


class TestParser(unittest.TestCase):
    def test_parse_lines_a_instruction(self):
        parser = Parser()
        lines_to_parse = ['@R0']

        parsed_lines = parser.parse(lines_to_parse)

        self.assertEqual(parsed_lines, [AInstruction('R0')])

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




if __name__ == '__main__':
    unittest.main()
