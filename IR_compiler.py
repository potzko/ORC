import orc_parser

class ir:
    def __init__(self) -> None:
        self.tmp_count = -1
        self.lable_count = -1

    def create_tmp(self):
        self.tmp_count += 1
        return f"@{self.tmp_count}"
    
    def create_lable(self):
        self.lable_count += 1
        return f"L@{self.lable_count}"

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
    
    def And(self, r0, r1, r2):
        return f'and {r0} {r1} {r2}\n'
    
    def Or(self, r0, r1, r2):
        return f'Or {r0} {r1} {r2}\n'
    
    def Xor(self, r0, r1, r2):
        return f'Xor {r0} {r1} {r2}\n'

    def neg(self, r0, r1):
        return f'neg {r0} {r1}\n'
    
    def Not(self, r0, r1):
        return f'not {r0} {r1}\n'
    
    def copy(self, r0, r1):
        return f'copy {r0} {r1}\n'
    
    def read(self, r0, r1):
        return f"read {r0} {r1}\n"
    
    def write(self, r0, r1):
        return f'write {r0} {r1}\n'
    
    def eq(self, r0, r1, r2):
        return f'eq {r0} {r1} {r2}\n'
    
    def ifnz(self, r0, lable):
        return f'ifnz {r0} {lable}\n'
    
    def fcall(self, r0, r1, r2):
        return f'fcall {r0} {r1} {r2}\n'

    def ret(self, r0):
        return f'ret {r0}\n'
    
    def nop(self):
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
        #single expressions
        case 'identifier':
            ret += ir_factory.init(output_reg, exp[1], '0')
        case 'literal_num':
            ret += ir_factory.mov(output_reg, exp[1])
        #binary expressions
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
        case '^':
            tmp1 , tmp2 = ir_factory.create_tmp(), ir_factory.create_tmp()
            ret += expression(tmp1, exp[1])
            ret += expression(tmp2, exp[2])
            ret += ir_factory.Xor(output_reg, tmp1, tmp2)
        case '&&':
            tmp1 , tmp2 = ir_factory.create_tmp(), ir_factory.create_tmp()
            ret += expression(tmp1, exp[1])
            ret += expression(tmp2, exp[2])
            ret += ir_factory.And(output_reg, tmp1, tmp2)
        case '||':
            tmp1 , tmp2 = ir_factory.create_tmp(), ir_factory.create_tmp()
            ret += expression(tmp1, exp[1])
            ret += expression(tmp2, exp[2])
            ret += ir_factory.Or(output_reg, tmp1, tmp2)
        
        #unary expressions
        case "unary_op":
            match exp[1]:
                case '+': ret += ir_factory.nop()
                case '-': ret += expression(output_reg, exp[2]) + ir_factory.neg(output_reg, output_reg)
                case '&': ret += expression(output_reg, exp[2]) + ir_factory.read(output_reg, output_reg)
                case '!': ret += expression(output_reg, exp[2]) + ir_factory.Not(output_reg, output_reg)
                #todo *
#\+|-|&|\*|\!

    return ret


code = """
2 && 3 || !-2;
"""
parser = orc_parser.parser(code)

parsed_code = parser.statement()
print(parsed_code)
print(statement(parsed_code))
