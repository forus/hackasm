import re

def assemble(asm):
    return '\n'.join([
        _assemble_line(_strip_asm_line(line))
        for line in asm.splitlines()
        if _strip_asm_line(line)])


def _strip_asm_line(asm):
    no_comment_asm = re.sub('//.*$', '', asm)
    return re.sub('\s+', '', no_comment_asm)


def _assemble_line(asm):
    if asm.startswith('@'):
        address = asm.lstrip('@')
        if address in _predefined_address_symbols:
            val = _predefined_address_symbols[address]
        elif address.isdigit():
            val = int(address)
        else:
            raise ValueError('"{}" address symbol is not defined.'.format(address))
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


_predefined_address_symbols = {
    'SP': 0,
    'LCL': 1,
    'ARG': 2,
    'THIS': 3,
    'THAT': 4,
    'R1': 1,
    'R2': 2,
    'R3': 3,
    'R4': 4,
    'R5': 5,
    'R6': 6,
    'R7': 7,
    'R8': 8,
    'R9': 9,
    'R10': 10,
    'R11': 11,
    'R12': 12,
    'R13': 13,
    'R14': 14,
    'R15': 15,
    'SCREEN': 16384,
    'KBD': 24576,
}


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
