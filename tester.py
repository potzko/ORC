import json
import rdp_parser
from tok import *
def ty(**kwargs):
    return kwargs

def cmp_json(a,b):
    return json.dumps(a) == json.dumps(b)

def test_batch(codes, res):
    a = rdp_parser.parser()
    for i in codes:
        assert cmp_json(a.parse(i), res)

def test_one(code, res):
    a = rdp_parser.parser()

    assert cmp_json(a.parse(code), res)


def test_literals():
    codes = [
    '123;', '    123;', '   123;', '  //asdasdasd\n123;', '/*asdasdasd\n\n\n\n\nasdasdasd*///\n//\n//\n\n\n\n\n123;']
    res = {
    "type": "Program",
    "body": [
            {
                "type": "ExpressionStatement",
                "Expression": {
                    "type": "NumericLiteral",
                    "value": 123
                }
            }
        ]
    }
    test_batch(codes, res)

    codes = [
    '"123;";', '    "123;";', '   "123;";', '  //asdasdasd\n"123;";', '/*asdasdasd\n\n\n\n\nasdasdasd*///\n//\n//\n\n\n\n\n"123;";']
    res = {
        "type": "Program",
        "body": [
            {
                "type": "ExpressionStatement",
                "Expression": {
                    "type": "StringLiteral",
                    "value": "123;"
                }
            }
        ]
    }
    test_batch(codes, res)

def test_blocks():
    codes = [
    '123;', '    123;', '   123;', '  //asdasdasd\n123;', '/*asdasdasd\n\n\n\n\nasdasdasd*///\n//\n//\n\n\n\n\n123;']
    res = {
    "type": "Program",
    "body": [
            {
                "type": "ExpressionStatement",
                "Expression": {
                    "type": "NumericLiteral",
                    "value": 123
                }
            }
        ]
    }
    test_batch(codes, res)

test_literals()