import json
import tok
from ASL_factorys import *

factory = ast_factory

class parser:
    def __init__(self) -> None:
        self.tokens = tok.tokenizer('')

    def parse(self, st):
        self.st = st
        self.tokens.st = self.st
        self.tokens.ind = 0
        return self.main()
     
    @property
    def  look_ahead(self):
        return self.tokens.next_token()


    def main(self):
        return self.program()
    
    def program(self):
        return factory.program(self.statment_list())
    
    # either a statement or a statment list
    def statment_list(self, stop = None):
        ret = []
        while (self.look_ahead != None) and self.look_ahead['type'] != stop:
            ret.append(self.statment())
        return ret

    def statment(self):
        match self.look_ahead['type']:
            case '{':
                a = self.block_statement()
            case ';':
                a = self.empty_statement()
            case _:
                a = self.expression_statement()
        return a

    def empty_statement(self):
        self.tokens.eat(';')
        return factory.empty_statement()

    def block_statement(self):
        self.tokens.eat('{')
        body = []
        if not self.look_ahead['type'] == '}':
            body = self.statment_list(stop='}')
        self.tokens.eat('}')
        return factory.block_statement(body)

    def expression_statement(self):
        ret = self.expression()
        self.tokens.eat(';')
        return factory.expression_statement(ret)

    def expression(self):
        return self.literal()

    def string_literal(self):
        return factory.string_literal(self.tokens.eat('StringLiteral'))

    def numeric_literal(self):
        return factory.numeric_literal(self.tokens.eat('NumericLiteral'))
    
    def literal(self):
        match self.look_ahead['type']:
            case "NumericLiteral":
                return self.numeric_literal()
            case "StringLiteral":
                return self.string_literal()
            case _:
                raise Exception(f'non supported literal type, found {self.look_ahead}')

code ="""
{
    {
        123;;
        321;
        "123";
        '321';
    }
}
"""

if __name__ == '__main__':
    code = parser().parse(code)
    code = factory.pretty(code)
    with open('a.json', 'w') as a:
        print(code)
        a.write(str(code))