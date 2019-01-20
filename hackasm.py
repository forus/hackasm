import re


def assemble(asm):
    stripped_lines = _strip_asm(asm)
    labelless_lines, label_symbol_to_code_address = _strip_labels(stripped_lines)
    variable_symbols = {}
    code_lines = [ _assemble_line(line, variable_symbols, label_symbol_to_code_address) for line in labelless_lines ]
    return '\n'.join(code_lines)


def _strip_asm(asm):
    for line in asm.splitlines():
        stripped_line = _strip_asm_line(line)
        if stripped_line:
            yield stripped_line


def _strip_labels(stripped_lines):
    labelless_lines = []
    label_symbol_to_code_address = {}
    for line in stripped_lines:
        if line.startswith('(') and line.endswith(')'):
            label = line.lstrip('(').rstrip(')')
            if label in _predefined_address_symbols:
                raise ValueError('"{}" is predefined symbol. Hence cannot be label name.'.format(label))
            label_symbol_to_code_address[label] = len(labelless_lines)
        else:
            labelless_lines.append(line)
    return labelless_lines, label_symbol_to_code_address


def _strip_asm_line(asm):
    no_comment_asm = re.sub('//.*$', '', asm)
    return re.sub('\s+', '', no_comment_asm)


def _assemble_line(asm, var_to_address, label_to_code_address):
    if asm.startswith('@'):
        return _assemble_address_line(asm, var_to_address, label_to_code_address)
    return _assemble_command_line(asm)


def _assemble_address_line(asm, var_to_address, label_to_code_address):
    address = asm.lstrip('@')
    if address.isdigit():
        val = int(address)
    elif address in _predefined_address_symbols:
        val = _predefined_address_symbols[address]
    elif address in label_to_code_address:
        val = label_to_code_address[address]
    elif address in var_to_address:
        val = var_to_address[address]
    else:
        var_to_address[address] = len(var_to_address) + 16
        val = var_to_address[address]
    return '{0:016b}'.format(val)


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


def _assemble_command_line(asm):
    asm_dest, asm_comp, asm_jump = _to_c_command_parts(asm)
    dest_code = _to_dest_code(asm_dest)
    comp_code, a = _to_comp_code_and_a_flag(asm_comp)
    jump_code = _to_jump_code(asm_jump)
    return '111{}{}{}{}'.format(a, comp_code, dest_code, jump_code)


def _to_c_command_parts(asm):
    if '=' in asm:
        asm_dest, asm_comp_jump = asm.split('=')
    else:
        asm_dest = 'null'
        asm_comp_jump = asm
    if ';' in asm_comp_jump:
        asm_comp, asm_jump = asm_comp_jump.split(';')
    else:
        asm_comp = asm_comp_jump
        asm_jump = 'null'
    return asm_dest, asm_comp, asm_jump


def _to_dest_code(asm_dest):
    if asm_dest == 'null':
        return '000'
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


def _to_comp_code_and_a_flag(asm_comp):
    if asm_comp in _comp_a_symbol_to_code:
        comp_code = _comp_a_symbol_to_code[asm_comp]
        a = '0'
    elif asm_comp in _comp_m_symbol_to_code:
        comp_code = _comp_m_symbol_to_code[asm_comp]
        a = '1'
    else:
        raise ValueError('Symbol "' + str(asm_comp) + '" is not known.')
    return comp_code, a


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


def _to_jump_code(asm_jump):
    if asm_jump in _jumps:
        jump_code = _jumps[asm_jump]
    elif asm_jump:
        raise ValueError('"{}" jump is not supported.'.format(asm_jump))
    return jump_code


_jumps = {
    'null': '000',
    'JGT': '001',
    'JEQ': '010',
    'JGE': '011',
    'JLT': '100',
    'JNE': '101',
    'JLE': '110',
    'JMP': '111',
}
