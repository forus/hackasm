comp_a_symbol_to_code = {
            '0': '101010',
            '1': '111111',
            '-1': '111010',
            'D': '001100',
            'A': '110000',
            '!D': '001101',
            '!A': '110001',
            '-D': '001111',
            '-A': '110011',
            'D+1': '011111',
            'A+1': '110111',
            'D-1': '001110',
            'A-1': '110010',
            'D+A': '000010',
            'D-A': '010011',
            'A-D': '000111',
            'D&A': '000000',
            'D|A': '010101',
        }
def assemble(asm):
    if asm.startswith('@'):
        val = int(asm.lstrip('@'))
        return '{0:016b}'.format(val)
    comp = comp_a_symbol_to_code[asm]
    return '1110{}000000'.format(comp)
