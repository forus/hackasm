import unittest
import hackasm

class HackAsmTestCase(unittest.TestCase):


    def test_a_command_gets_assembled(self):
        code = hackasm.assemble('@5')
        self.assertEqual(code, '0000000000000101')


    def test_a_min_val_gets_assembled(self):
        code = hackasm.assemble('@0')
        self.assertEqual(code, '0' * 16)


    def test_a_max_val_gets_assembled(self):
        code = hackasm.assemble('@' + str(2 ** 16 - 1))
        self.assertEqual(code, '1' * 16)


    def test_zero_c_command(self):
        code = hackasm.assemble('0')
        self.assertEqual(code, '111' + '0' + '101010' + '000' + '000')


    def test_one_c_command(self):
        code = hackasm.assemble('1')
        self.assertEqual(code, '111' + '0' + '111111' + '000' + '000')


if __name__ == '__main__':
    unittest.main()
