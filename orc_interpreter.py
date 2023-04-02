import orc_parser
code = """
fn main a,b:{
    print("hi mom");
    return "hello world";
}
"""
parser = orc_parser.orc_parser()
st = parser.parse(code=code)

class orc_interpreter:
    def __init__(self) -> None:
        self.functions = {}
    
    def interpret(self, node, scope = None):
        if scope == None:
            scope = {}
        print(node)
        match node[0]:
            case 'fn_block'         : return self.interpret_module(node)
            case 'literal_string'   : return self.literal_string()
            case 'return'           : return node[1][1]
            case 'call'             : return self.fn_call(node,scope)


    def interpret_module(self, node):
        for function_dec in node[1:]:
            self.functions[function_dec[1][1]] = function_dec
        return self.interpret(self.functions['main'][3], scope={})

    def literal_string(self, node):
        return node(1)
    
    def fn_call(self, node):
        print('a')
        func = self.functions[node[1]]
        args = {name[1]: self.interpret(value) for name, value in zip(func[2][1],node[2][1])}
        for i in func[4]:
            self.interpret(func[3], args)

interpreter = orc_interpreter()
print(interpreter.interpret(st))
print(interpreter.functions['main'])