comp_a_symbol_to_code = {
            '0': '101010',
            '1': '111111',
        }
def assemble(asm):
    if asm.startswith('@'):
        val = int(asm.lstrip('@'))
        return '{0:016b}'.format(val)
    comp = comp_a_symbol_to_code[asm]
    return '1110{}000000'.format(comp)
