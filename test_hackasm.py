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


    def test_m_c_command(self):
        self._test_c_command_comp(comp='M', a='1', code='110000')


    def test_not_m_c_command(self):
        self._test_c_command_comp(comp='!M', a='1', code='110001')


    def test_minus_m_c_command(self):
        self._test_c_command_comp(comp='-M', a='1', code='110011')


    def test_m_plus_one_c_command(self):
        self._test_c_command_comp(comp='M+1', a='1', code='110111')


    def test_m_minus_one_c_command(self):
        self._test_c_command_comp(comp='M-1', a='1', code='110010')


    def test_d_plus_m_c_command(self):
        self._test_c_command_comp(comp='D+M', a='1', code='000010')


    def test_d_minus_m_c_command(self):
        self._test_c_command_comp(comp='D-M', a='1', code='010011')


    def test_m_minus_d_c_command(self):
        self._test_c_command_comp(comp='M-D', a='1', code='000111')


    def test_d_and_m_c_command(self):
        self._test_c_command_comp(comp='D&M', a='1', code='000000')


    def test_d_or_m_c_command(self):
        self._test_c_command_comp(comp='D|M', a='1', code='010101')


    def _test_c_command_comp(self, comp, a, code):
        actual_code = hackasm.assemble(comp)
        self.assertEqual(actual_code, '111' + a + code + '000' + '000')


    def test_unknown_c_command(self):
        with self.assertRaises(ValueError) as err:
            hackasm.assemble('U')
        self.assertEqual(str(err.exception), 'Symbol "U" is not known.')


    def test_a_destination(self):
        actual_code = hackasm.assemble('A=0')
        self.assertEqual(actual_code[10:13], '100')


    def test_m_destination(self):
        actual_code = hackasm.assemble('M=0')
        self.assertEqual(actual_code[10:13], '010')


    def test_d_destination(self):
        actual_code = hackasm.assemble('D=0')
        self.assertEqual(actual_code[10:13], '001')


    def test_invalid_destination(self):
        with self.assertRaises(ValueError) as err:
            hackasm.assemble('X=0')
        self.assertEqual(str(err.exception), '"X" is wrong destination.')

    def test_repeated_destination(self):
        with self.assertRaises(ValueError) as err:
            hackasm.assemble('AMA=0')
        self.assertEqual(str(err.exception), '"A" destination appears multiple times.')


    def test_jgt_jump(self):
        actual_code = hackasm.assemble('0;JGT')
        self.assertEqual(actual_code[13:], '001')


    def test_jeq_jump(self):
        actual_code = hackasm.assemble('0;JEQ')
        self.assertEqual(actual_code[13:], '010')


    def test_jge_jump(self):
        actual_code = hackasm.assemble('0;JGE')
        self.assertEqual(actual_code[13:], '011')


    def test_jlt_jump(self):
        actual_code = hackasm.assemble('0;JLT')
        self.assertEqual(actual_code[13:], '100')


    def test_jne_jump(self):
        actual_code = hackasm.assemble('0;JNE')
        self.assertEqual(actual_code[13:], '101')


    def test_jle_jump(self):
        actual_code = hackasm.assemble('0;JLE')
        self.assertEqual(actual_code[13:], '110')


    def test_jmp_jump(self):
        actual_code = hackasm.assemble('0;JMP')
        self.assertEqual(actual_code[13:], '111')


if __name__ == '__main__':
    unittest.main()
