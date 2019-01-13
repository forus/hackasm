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


    def test_minus_one_c_command(self):
        self._test_c_command_comp(comp='-1', a='0', code='111010')


    def test_d_c_command(self):
        self._test_c_command_comp(comp='D', a='0', code='001100')


    def test_a_c_command(self):
        self._test_c_command_comp(comp='A', a='0', code='110000')


    def test_not_d_c_command(self):
        self._test_c_command_comp(comp='!D', a='0', code='001101')


    def test_not_a_c_command(self):
        self._test_c_command_comp(comp='!A', a='0', code='110001')


    def test_minus_d_c_command(self):
        self._test_c_command_comp(comp='-D', a='0', code='001111')


    def test_minus_a_c_command(self):
        self._test_c_command_comp(comp='-A', a='0', code='110011')


    def test_d_plus_one_c_command(self):
        self._test_c_command_comp(comp='D+1', a='0', code='011111')


    def test_a_plus_one_c_command(self):
        self._test_c_command_comp(comp='A+1', a='0', code='110111')


    def test_d_minus_one_c_command(self):
        self._test_c_command_comp(comp='D-1', a='0', code='001110')


    def test_a_minus_one_command(self):
        self._test_c_command_comp(comp='A-1', a='0', code='110010')


    def test_d_plus_a_c_command(self):
        self._test_c_command_comp(comp='D+A', a='0', code='000010')


    def test_d_minus_a_c_command(self):
        self._test_c_command_comp(comp='D-A', a='0', code='010011')


    def test_a_minus_d_c_command(self):
        self._test_c_command_comp(comp='A-D', a='0', code='000111')


    def test_d_and_a_c_command(self):
        self._test_c_command_comp(comp='D&A', a='0', code='000000')


    def test_d_or_a_c_command(self):
        self._test_c_command_comp(comp='D|A', a='0', code='010101')


    def _test_c_command_comp(self, comp, a, code):
        actual_code = hackasm.assemble(comp)
        self.assertEqual(actual_code, '111' + a + code + '000' + '000')

if __name__ == '__main__':
    unittest.main()
