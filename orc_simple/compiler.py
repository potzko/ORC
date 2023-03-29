import parser
def output(a,b,c):
    #print(f"{a:10} {b:10} {c:10}")
    return f"{a:10} {b:10} {c:10}"

class compiler:
    def __init__(self) -> None:
        self.p = parser.parser()
    
    def compile(self, code):
        ret = []
        ret.append(output("global", "_start", ""))
        ret.append(output("section", ".text", ""))
        ret.append(output("_start", "_start", ""))
        ast = self.p.parse(code=code)
        print(ast)
        for node in ast:
            token_type, arguments = ast[0], ast[1:]
        print('\n'.join(ret))



a = compiler()

a.compile("a,b;")
