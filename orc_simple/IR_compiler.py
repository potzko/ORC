import orc_parser

tmp = [-1]
class ir:
    def create_tmp():
        tmp[0] += 1
        return f"@{tmp[0]}"

    def init(self, r0, sym, literal):
        return f'init {r0} {sym} {literal}\n'
    
    def add(self, r0, r1, r2):
        return f'add {r0} {r1} {r2}\n'
    
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
    
ir_factory = ir

class statement:
    def init(self, st, next):
        self.next = next
        if len(st) == 0:
            self.ops = ir_factory.nop()
            return

class expression:
    def __init__(self, exp, output_reg) -> None:
        if len(exp) == 0:
            raise Exception('a')

        match exp[0]:
            case '+':
                self.ops = ir_factory.copy(ir_factory.create_tmp(), expression)     


class ir_compiler:
    def __init__(self) -> None:
        self.values = {}

    def compile(self, code):
        if len(code) == 0:
            self.ops = ir_factory.nop()
            return
        match code[0]:
            case 'add': self.ops 

    


        