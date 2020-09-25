import unittest
from assembler import SymbolTable


class TestSymbolTable(unittest.TestCase):

    def test_get_builtin_symbol(self):
        symbolTable = SymbolTable()

        self.assertEqual(symbolTable.getSymbolValue('R0'), 0)


if __name__ == '__main__':
    unittest.main()
