import orc_parser

class ir:
    def __init__(self) -> None:
        self.tmp_count = -1

    def create_tmp(self):
        self.tmp_count += 1
        return f"@{self.tmp_count}"

    def mov(self, r0, literal):
        return f'mov {r0} {literal}\n'

    def init(self, r0, sym, literal):
        return f'init {r0} {sym} {literal}\n'
    
    def add(self, r0, r1, r2):
        return f'add {r0} {r1} {r2}\n'
    
    def mul(self, r0, r1, r2):
        return f'mul {r0} {r1} {r2}\n'
    
    def div(self, r0, r1, r2):
        return f'div {r0} {r1} {r2}\n'
    
    def mod(self, r0, r1, r2):
        return f'mod {r0} {r1} {r2}\n'
    
    def neg(self, r0, r1):
        return f'neg {r0} {r1}\n'
    
    def copy(r0, r1):
        return f'copy {r0} {r1}\n'
    
    def read(r0, r1):
        return f"read {r0} {r1}\n"
    
    def write(r0, r1):
        return f'write {r0} {r1}\n'
    
    def eq(r0, r1, r2):
        return f'eq {r0} {r1} {r2}\n'
    
    def ifnz(r0, lable):
        return f'ifnz {r0} {lable}\n'
    
    def fcall(r0, r1, r2):
        return f'fcall {r0} {r1} {r2}\n'

    def ret(r0):
        return f'ret {r0}\n'
    
    def nop():
        return f'nop\n'
    
ir_factory = ir()

def statement(node):
    if not node:
        return ir_factory.nop()
    
    ret = ''
    match node[0]:
        case 'statement_list':
            for i in node[1:]:
                ret += statement(i)
        case _:
            ret += expression(ir_factory.create_tmp() ,node)
    
    return ret

    
    

def expression(output_reg, exp) -> None:
    if len(exp) == 0:
        return ir_factory.nop()

    ret = ''
    match exp[0]: 
        case 'identifier':
            ret += ir_factory.init(output_reg, exp[1], '0')
        case 'literal_num':
            ret += ir_factory.mov(output_reg, exp[1])
        case '+':
            tmp1 , tmp2 = ir_factory.create_tmp(), ir_factory.create_tmp()
            ret += expression(tmp1, exp[1])
            ret += expression(tmp2, exp[2])
            ret += ir_factory.add(output_reg, tmp1, tmp2)
        case '-':
            tmp1 , tmp2 = ir_factory.create_tmp(), ir_factory.create_tmp()
            ret += expression(tmp1, exp[1])
            ret += expression(tmp2, exp[2])
            ret += ir_factory.neg(tmp2, tmp2)
            ret += ir_factory.add(output_reg, tmp1, tmp2)
        case '*':
            tmp1 , tmp2 = ir_factory.create_tmp(), ir_factory.create_tmp()
            ret += expression(tmp1, exp[1])
            ret += expression(tmp2, exp[2])
            ret += ir_factory.mul(output_reg, tmp1, tmp2)
        case '/':
            tmp1 , tmp2 = ir_factory.create_tmp(), ir_factory.create_tmp()
            ret += expression(tmp1, exp[1])
            ret += expression(tmp2, exp[2])
            ret += ir_factory.div(output_reg, tmp1, tmp2)
        case '%':
            tmp1 , tmp2 = ir_factory.create_tmp(), ir_factory.create_tmp()
            ret += expression(tmp1, exp[1])
            ret += expression(tmp2, exp[2])
            ret += ir_factory.mod(output_reg, tmp1, tmp2)


    return ret


code = """
2 * 3 - (1 + 4) % 5;
"""
parser = orc_parser.parser(code)

parsed_code = parser.statement()

print(statement(parsed_code))
