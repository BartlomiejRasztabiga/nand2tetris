import unittest
from assembler import SymbolTable


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


if __name__ == '__main__':
    unittest.main()
