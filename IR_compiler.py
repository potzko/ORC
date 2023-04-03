import orc_parser

class ir:
    def __init__(self) -> None:
        self.tmp_count = -1
        self.lable_count = -1
        self.Mov = self._construct('mov', 2)
        self.Init = self._construct('init', 3)
        self.Add = self._construct('add', 3)
        self.Mul = self._construct('mul', 3)
        self.Div = self._construct('div', 3)
        self.Mod = self._construct('mod', 3)
        self.And = self._construct('and', 3)
        self.Or = self._construct('or', 3)
        self.Xor = self._construct('xor', 3)
        self.Fcall = self._construct("fcall", 3)
        self.Neg = self._construct("neg", 2)
        self.Not = self._construct("not", 2)
        self.Copy = self._construct("copy", 2)
        self.Read = self._construct("read", 2)
        self.Write = self._construct("write", 2) 
        self.Neq = self._construct("neq", 3)
        self.Eq = self._construct("eq", 3)
        self.Ifnz = self._construct("ifnz", 2)
        self.Ret = self._construct("ret", 1)
        self.Jmp = self._construct("jmp", 1)
        self.Nop = self._construct("nop", 0)
        self.Setb = self._construct("setb", 3)
        self.Setbe = self._construct("setbe", 3)

    def create_tmp(self):
        self.tmp_count += 1
        return f"@{self.tmp_count}"
    
    def create_lable(self):
        self.lable_count += 1
        return f"L@{self.lable_count}"
    
    def _construct(self, st, val_count):
        ret_str = f'{st:10} ' + ' {:7}'*val_count + '\n'
        def ret(*args):
            if len(args) != val_count:
                raise Exception(f'expected {val_count} variables, found {len(args)} instead')
            return ret_str.format(*args)
        return ret

    def lable(self, l):
        return l + '\n'
    
ir_factory = ir()


def statement(node):
    if not node:
        return ir_factory.Nop()
    
    primary, *secondary = node
    ret = ''
    match primary:
        case "statement_list": ret += "".join(map(statement, secondary))
        case "if":
            cond = ir_factory.create_tmp()
            cond_eval = expression(cond, node[1])
            state_true = statement(node[2])
            state_false = statement(node[3])
            block_true = ir_factory.create_lable()
            block_end = ir_factory.create_lable()

            ret += cond_eval
            ret += ir_factory.Ifnz(cond, block_true)
            ret += state_false
            ret += ir_factory.Jmp(block_end)
            ret += ir_factory.lable(block_true)
            ret += state_true
            ret += ir_factory.lable(block_end)
        case "while":
            cond = ir_factory.create_tmp()
            cond_eval = expression(cond, node[1])
            state_true = statement(node[2])
            block_loop = ir_factory.create_lable()
            block_loop_start = ir_factory.create_lable()
            block_end = ir_factory.create_lable()

            ret += ir_factory.lable(block_loop)
            ret += cond_eval
            ir_factory.Ifnz(cond, block_loop_start)
            ret += ir_factory.Jmp(block_end)
            ret += ir_factory.lable(block_loop_start)
            ret += state_true
            ret += ir_factory.Jmp(block_loop)
            ret += ir_factory.lable(block_end)

        case  _: ret += expression(ir_factory.create_tmp() ,node)
    return ret

    
    

def expression(output_reg, exp) -> None:
    if len(exp) == 0:
        return ir_factory.nop()

    ret = ''
    match exp[0]:
        #single expressions
        case 'identifier':
            ret += ir_factory.Init(output_reg, exp[1], '0')
        case 'literal_num':
            ret += ir_factory.Mov(output_reg, exp[1])
        #binary expressions
        case '+':
            tmp1 , tmp2 = ir_factory.create_tmp(), ir_factory.create_tmp()
            ret += expression(tmp1, exp[1])
            ret += expression(tmp2, exp[2])
            ret += ir_factory.Add(output_reg, tmp1, tmp2)
        case '-':
            tmp1 , tmp2 = ir_factory.create_tmp(), ir_factory.create_tmp()
            ret += expression(tmp1, exp[1])
            ret += expression(tmp2, exp[2])
            ret += ir_factory.Neg(tmp2, tmp2)
            ret += ir_factory.Add(output_reg, tmp1, tmp2)
        case '*':
            tmp1 , tmp2 = ir_factory.create_tmp(), ir_factory.create_tmp()
            ret += expression(tmp1, exp[1])
            ret += expression(tmp2, exp[2])
            ret += ir_factory.Mul(output_reg, tmp1, tmp2)
        case '/':
            tmp1 , tmp2 = ir_factory.create_tmp(), ir_factory.create_tmp()
            ret += expression(tmp1, exp[1])
            ret += expression(tmp2, exp[2])
            ret += ir_factory.Div(output_reg, tmp1, tmp2)
        case '%':
            tmp1 , tmp2 = ir_factory.create_tmp(), ir_factory.create_tmp()
            ret += expression(tmp1, exp[1])
            ret += expression(tmp2, exp[2])
            ret += ir_factory.Mod(output_reg, tmp1, tmp2)
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
        case '==':
            tmp1 , tmp2 = ir_factory.create_tmp(), ir_factory.create_tmp()
            ret += expression(tmp1, exp[1])
            ret += expression(tmp2, exp[2])
            ret += ir_factory.Eq(output_reg, tmp1, tmp2)
        case '<':
            tmp1 , tmp2 = ir_factory.create_tmp(), ir_factory.create_tmp()
            ret += expression(tmp1, exp[1])
            ret += expression(tmp2, exp[2])
            ret += ir_factory.Setb(output_reg, tmp1, tmp2)
        case '>':
            tmp1 , tmp2 = ir_factory.create_tmp(), ir_factory.create_tmp()
            ret += expression(tmp2, exp[1])
            ret += expression(tmp1, exp[2])
            ret += ir_factory.Setb(output_reg, tmp1, tmp2)
        case '<=':
            tmp1 , tmp2 = ir_factory.create_tmp(), ir_factory.create_tmp()
            ret += expression(tmp1, exp[1])
            ret += expression(tmp2, exp[2])
            ret += ir_factory.Setbe(output_reg, tmp1, tmp2)
        case '>=':
            tmp1 , tmp2 = ir_factory.create_tmp(), ir_factory.create_tmp()
            ret += expression(tmp2, exp[1])
            ret += expression(tmp1, exp[2])
            ret += ir_factory.Setbe(output_reg, tmp1, tmp2)
        case '!=':
            tmp1 , tmp2 = ir_factory.create_tmp(), ir_factory.create_tmp()
            ret += expression(tmp1, exp[1])
            ret += expression(tmp2, exp[2])
            ret += ir_factory.Neq(output_reg, tmp1, tmp2)
        
        #unary expressions
        case "unary_op":
            match exp[1]:
                case '+': ret += ir_factory.nop()
                case '-': ret += expression(output_reg, exp[2]) + ir_factory.Neg(output_reg, output_reg)
                case '&': ret += expression(output_reg, exp[2]) + ir_factory.Read(output_reg, output_reg)
                case '!': ret += expression(output_reg, exp[2]) + ir_factory.Not(output_reg, output_reg)
                case _: raise Exception(f'oh nyo :3')
        
        case _:
            raise Exception(f'oh nyo')
#\+|-|&|\!
    return ret


code = """
a + 5 = 3;
"""
parser = orc_parser.parser(code)

parsed_code = parser.statement_list()
print(parsed_code)
print(statement(parsed_code))
