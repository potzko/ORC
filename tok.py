import re
import json as js
def ty(**kwargs):
    return kwargs

spec = [
    # white space
    (r'( +)'         , None),
    # new line
    (r'(\n)'         , None),
    # comments
    (r'(//[^\n]*)\n' , None),
    (r'(/\*[^/]*/)'  , None),

    # int literal
    (r'([0-9]+)'  , 'NumericLiteral'),
    # string literal
    (r'"([^"]*)"' , 'StringLiteral'),
    (r"'([^']*)'" , 'StringLiteral'),

    #addative ops
    (r"(\+|-)"      , 'AdditiveOperator'),

    #multiplicative ops
    (r"(\*|\/|\%)"   , 'MultiplicativeOperator'),

    # delimiters
    (r"(;)"       , ';'),
    (r"({)"       , '{'),
    (r"(})"       , '}'),
    (r"(\()"       , '('),
    (r"(\))"       , ')'),
]

class tokenizer:
    def __init__(self, st) -> None:
        self.st = st
        self.ind = 0

    def reset(self, st):
        self.st = st
        self.ind = 0

    def has_next_token(self):
        return self.ind < len(self.st)

    def next_token(self, return_value = 1):
        st = self.st[self.ind:]
        matches = ((mat, exp, type) for exp, type in spec if (mat := re.match(exp, st)))
        
        for mat, exp, type in matches:
            if type == None:
                self.ind += len(mat.group(1))
                return self.next_token()
            return ty(type = type, value = mat.group(return_value))

        if self.ind == len(self.st):
            return None
        raise Exception(f'could not tokenize {self.st}')

    def eat(self, tock_type):
        ret = self.next_token(return_value=1)
        if ret == None:
            a = f'unexpected file end, expected {tock_type}'
            raise Exception(a)
        if ret['type'] != tock_type:
            a = 'unexpected token. expected {0} found {1} instead'.format(tock_type, ret)
            raise Exception(a)
        point_len = len(self.next_token(return_value=0)['value'])
        self.ind += point_len

        return ret['value']