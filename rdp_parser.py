import json
import tok
from ASL_factorys import *

factory = s_exp_factory
factory = ast_factory

class parser:
    def __init__(self) -> None:
        self.tokens = tok.tokenizer('')

    def parse(self, st):
        self.st = st
        self.tokens.reset(self.st)
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
        return self.addative_expression()
    
    def addative_expression(self):
        return self.binary_expression(self.multiplicative_expression, 'AdditiveOperator')
    
    def multiplicative_expression(self):
        return self.binary_expression(self.primary_expression, 'MultiplicativeOperator')
    
    def binary_expression(self, op_type, op_token):
        left = op_type()
        while self.look_ahead['type'] == op_token:
            operator = self.tokens.eat(op_token)
            right = op_type()
            left = factory.additive_operator(left, right, operator)
        return left


    def primary_expression(self):
        match self.look_ahead['type']:
            case '(':
                return self.parenthesized_expression()
            case _:
                return self.literal()

    def parenthesized_expression(self):
        self.tokens.eat('(')
        ret = self.expression()
        self.tokens.eat(')')
        return ret

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
(1 + 2 * 3 + (4 + 5) * 6) + 1 * 2;
"""

if __name__ == '__main__':
    code = parser().parse(code)
    code = factory.pretty(code)
    with open('a.json', 'w') as a:
        print(code)
        a.write(str(code))