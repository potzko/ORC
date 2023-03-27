import json
from jsonS import *
import tok

# ast factory
class ast_factory:
    def program(tree):
        return json.dumps(tree)

    def empty_statement():
        return ty(type = 'EmptyStatement')
    
    def block_statement(tree):
        return ty(type = 'BlockStatement', body = tree)
    
    def string_literal(tree):
        return ty(type = 'StringLiteral', value = tree)

    def numeric_literal(tree):
        return ty(type = 'NumericLiteral', value = int(tree))
    
    def expression_statement(tree):
        return ty(type = 'ExpressionStatement', Expression = tree)
 


# s expretion factory
class s_exp_factory:
    def program(tree):
        return ['begin', tree]
    
    def empty_statement():
        return {}

    def block_statement(tree):
        return ['begin', tree]

    def string_literal(tree):
        return f'"{tree}"'

    def numeric_literal(tree):
        return tree
    
    def expression_statement(tree):
        return tree
    

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
        return ty(type = 'Program', body = self.statment_list())
    
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
        return ty(type = 'EmptyStatement')

    def block_statement(self):
        self.tokens.eat('{')
        body = []
        if not self.look_ahead['type'] == '}':
            body = self.statment_list(stop='}')
        self.tokens.eat('}')
        return ty(type = 'BlockStatement', body = body)

    def expression_statement(self):
        ret = self.expression()
        self.tokens.eat(';')
        return(ret)

    def expression(self):
        return self.literal()

    def string_literal(self):
        return ty(type = 'StringLiteral', value = self.tokens.eat('StringLiteral'))

    def numeric_literal(self):
        return ty(type = 'NumericLiteral', value = int(self.tokens.eat('NumericLiteral')))
    
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
    print(parser().parse(code))
    with open('a.json', 'w') as a:
        #a.write(dp_print(parser().parse(code)))
        pass