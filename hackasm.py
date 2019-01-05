def assemble(asm):
    val = int(asm.lstrip('@'))
    return '{0:016b}'.format(val)
