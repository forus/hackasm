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


comp_m_symbol_to_code = {
            'M': '110000',
            '!M': '110001',
            '-M': '110011',
            'M+1': '110111',
            'M-1': '110010',
            'D+M': '000010',
            'D-M': '010011',
            'M-D': '000111',
            'D&M': '000000',
            'D|M': '010101',
        }


def assemble(asm):
    if asm.startswith('@'):
        val = int(asm.lstrip('@'))
        return '{0:016b}'.format(val)
    dest = ''
    if '=' in asm:
        dest, asm = asm.split('=')
    if asm in comp_a_symbol_to_code: 
        comp = comp_a_symbol_to_code[asm]
        a = '0'
    elif asm in comp_m_symbol_to_code:
        comp = comp_m_symbol_to_code[asm]
        a = '1'
    else:
        raise ValueError('Symbol "' + str(asm) + '" is not known.')
    dest_code = ''
    if 'A' in dest:
       dest_code += '1'
    else:
       dest_code += '0'
    if 'M' in dest:
       dest_code += '1'
    else:
       dest_code += '0'
    if 'D' in dest:
       dest_code += '1'
    else:
       dest_code += '0'

    return '111{}{}{}000'.format(a, comp, dest_code)
