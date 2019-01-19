import re

def assemble(asm):
    return '\n'.join([_assemble_line(_strip_asm_line(line)) for line in asm.splitlines() if line.strip()])


def _strip_asm_line(asm):
    return re.sub('\s+', '', asm)


def _assemble_line(asm):
    if asm.startswith('@'):
        val = int(asm.lstrip('@'))
        return '{0:016b}'.format(val)
    if '=' in asm:
        asm_dest, asm_comp_jump = asm.split('=')
    else:
        asm_dest = ''
        asm_comp_jump = asm
    if ';' in asm_comp_jump:
        asm_comp, asm_jump = asm_comp_jump.split(';')
    else:
        asm_comp = asm_comp_jump
        asm_jump = ''
    if asm_comp in _comp_a_symbol_to_code:
        comp_code = _comp_a_symbol_to_code[asm_comp]
        a = '0'
    elif asm_comp in _comp_m_symbol_to_code:
        comp_code = _comp_m_symbol_to_code[asm_comp]
        a = '1'
    else:
        raise ValueError('Symbol "' + str(asm_comp) + '" is not known.')

    if asm_jump in _jumps:
        jump_code = _jumps[asm_jump]
    elif asm_jump:
        raise ValueError('"{}" jump is not supported.'.format(asm_jump))
    else:
        jump_code = '000'

    dest_code = _to_dest_code(asm_dest)
    return '111{}{}{}{}'.format(a, comp_code, dest_code, jump_code)


_comp_a_symbol_to_code = {
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


_comp_m_symbol_to_code = {
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


_jumps = {
    'JGT': '001',
    'JEQ': '010',
    'JGE': '011',
    'JLT': '100',
    'JNE': '101',
    'JLE': '110',
    'JMP': '111',
}


def _to_dest_code(asm_dest):
    _check_dest(asm_dest)
    dest_code = ''
    if 'A' in asm_dest:
       dest_code += '1'
    else:
       dest_code += '0'
    if 'M' in asm_dest:
       dest_code += '1'
    else:
       dest_code += '0'
    if 'D' in asm_dest:
       dest_code += '1'
    else:
       dest_code += '0'

    return dest_code


def _check_dest(asm_dest):
    for indx, letter in enumerate(asm_dest):
        if letter not in 'AMD':
            raise ValueError('"{}" is wrong destination.'.format(letter))
        if indx < len(asm_dest) and letter in asm_dest[indx+1:]:
            raise ValueError('"{}" destination appears multiple times.'.format(letter))
