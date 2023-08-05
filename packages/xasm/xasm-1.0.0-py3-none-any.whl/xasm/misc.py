import time
from struct import pack
from xdis.magics import magics
from xdis import PYTHON3

def write_pycfile(pyc_file, asm):
    if PYTHON3:
        file_mode = 'wb'
    else:
        file_mode = 'w'

    with open(pyc_file, file_mode) as fp:
        fp.write(magics[asm.python_version])
        if not asm.timestamp :
            asm.timestamp = int(time.time())
        fp.write(pack('I', asm.timestamp))
        if asm.python_version > '3.2':
            fp.write(pack('I', asm.size))
        from xdis.marsh import dumps
        for co in asm.code_list:
            try:
                co_obj = dumps(co, python_version=asm.python_version)
                if PYTHON3 and asm.python_version < '3.0':
                    co_obj = str.encode(co_obj)
                    pass

                fp.write(co_obj)
            except:
                pass
            pass
    print("Wrote %s" % pyc_file)

def get_opcode(python_version):
    # not sure we can do < 2.5 yet.
    if python_version in "1.3 1.4 1.5".split():
        if python_version == '1.3':
            from xdis.code import Code13 as Code
            from xdis.opcodes import opcode_13 as opc
        elif python_version == '1.3':
            from xdis.code import Code14 as Code
            from xdis.opcodes import opcode_14 as opc
        elif python_version == '1.5':
            from xdis.code import Code2 as Code
            from xdis.opcodes import opcode_15 as opc
    elif python_version in "2.2 2.3 2.4 2.5 2.6 2.7".split():
        from xdis.code import Code2 as Code
        if python_version == '2.2':
            from xdis.opcodes import opcode_22 as opc
        elif python_version == '2.3':
            from xdis.opcodes import opcode_23 as opc
        elif python_version == '2.4':
            from xdis.opcodes import opcode_24 as opc
        elif python_version == '2.5':
            from xdis.opcodes import opcode_25 as opc
        elif python_version == '2.6':
            from xdis.opcodes import opcode_26 as opc
        else:
            from xdis.opcodes import opcode_27 as opc
            pass
    elif python_version in "3.2 3.3 3.4 3.5 3.6 3.7 3.8".split():
        from xdis.code import Code3 as Code
        if python_version == '3.0':
            from xdis.opcodes import opcode_30 as opc
        elif python_version == '3.1':
            from xdis.opcodes import opcode_31 as opc
        elif python_version == '3.2':
            from xdis.opcodes import opcode_32 as opc
        elif python_version == '3.3':
            from xdis.opcodes import opcode_33 as opc
        elif python_version == '3.4':
            from xdis.opcodes import opcode_34 as opc
        elif python_version == '3.5':
            from xdis.opcodes import opcode_35 as opc
        elif python_version == '3.6':
            from xdis.opcodes import opcode_36 as opc
        elif python_version == '3.7':
            from xdis.opcodes import opcode_37 as opc
        elif python_version == '3.8':
            from xdis.opcodes import opcode_38 as opc
    else:
        raise RuntimeError("Python version %s not supported yet" % python_version)
    return opc, Code
