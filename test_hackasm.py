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
        self._test_c_command_comp(comp='0', a='0', code='101010')


    def test_one_c_command(self):
        self._test_c_command_comp(comp='1', a='0', code='111111')


    def _test_c_command_comp(self, comp, a, code):
        actual_code = hackasm.assemble(comp)
        self.assertEqual(actual_code, '111' + a + code + '000' + '000')

if __name__ == '__main__':
    unittest.main()
