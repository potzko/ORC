import json
import rdp_parser
from tok import *

def cmp_json(a,b):
    return a == json.loads(b)

flag = True

parser = rdp_parser.parser()
codes = ['123;', '//   \n123;', '       123; ']
expected = json.dumps(ty(type = 'Program', body = [ty(type = 'NumericLiteral', value = 123)]))
for i in codes:
    tmp = parser.parse(i)
    flag = flag & (cmp_json(tmp, expected))
print(flag)
flag = True

codes = ['"123";', '//   \n"123";', '       "123";']
codes += ["'123';", "//   \n'123';", "       '123';"]
expected = json.dumps(ty(type = 'Program', body = [ty(type = 'StringLiteral', value = '123')]))
for i in codes:
    tmp = parser.parse(i)
    flag = flag & (cmp_json(tmp, expected))
print(flag)

codes = [
"""
123;
321;
"123";
'321';
"""
]
expected = json.dumps(ty(type = 'Program', body = [
    ty(type = 'NumericLiteral', value = 123),
    ty(type = 'NumericLiteral', value = 321),
    ty(type = 'StringLiteral', value = '123'),
    ty(type = 'StringLiteral', value = '321')
    ]))

for i in codes:
    tmp = parser.parse(i)
    flag = flag & (cmp_json(tmp, expected))
print(flag)

codes = [
"""
{
    123;
    321;
    "123";
    '321';
}
"""
]
expected = json.dumps(ty(type = 'Program', body = [ty(type = "BlockStatement", body = [
    ty(type = 'NumericLiteral', value = 123),
    ty(type = 'NumericLiteral', value = 321),
    ty(type = 'StringLiteral', value = '123'),
    ty(type = 'StringLiteral', value = '321')
])]))

for i in codes:
    tmp = parser.parse(i)
    flag = flag & (cmp_json(tmp, expected))
print(flag)

codes = [
"""
{

}
"""
]
expected = json.dumps(ty(type = 'Program', body = [ty(type = "BlockStatement", body = [])]))

for i in codes:
    tmp = parser.parse(i)
    flag = flag & (cmp_json(tmp, expected))
print(flag)

codes = [
"""
{
    {

    }
}
"""
]
expected = json.dumps(ty(type = 'Program', body = [ty(type = "BlockStatement", body = [ty(type = "BlockStatement", body = [ ])])]))

for i in codes:
    tmp = parser.parse(i)
    flag = flag & (cmp_json(tmp, expected))
print(flag)



codes = [
"""
{
    {
        123;;
        321;
        "123";
        '321';
    }
}
"""
]
expected = json.dumps(ty(type = 'Program', body = [ty(type = "BlockStatement", body = [ty(type = "BlockStatement", body = [
    ty(type = 'NumericLiteral', value = 123),
    {'type': 'EmptyStatement'},
    ty(type = 'NumericLiteral', value = 321),
    ty(type = 'StringLiteral', value = '123'),
    ty(type = 'StringLiteral', value = '321')
])])]))

for i in codes:
    tmp = parser.parse(i)
    flag = flag & (cmp_json(tmp, expected))
print(flag)