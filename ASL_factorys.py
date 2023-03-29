import json
def ty(**kwargs):
    return kwargs


# ast factory
class ast_factory:
    def get_type(node):
        return node['type']

    def pretty(tree):
        return json.dumps(tree, indent=4)

    def program(tree):
        return ty(type = 'Program', body = tree)

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
    
    def binary_operator(left, right, operator):
        return ty(type = 'BinaryExpression', left = left, right = right, operator = operator)
    
    def assignment_expression(left, right, operator):
        return ty(type = "Assignment_expression", left = left, right = right, operator = operator)
    
    def identifier(name):
        return ty(type = 'Identifier', name = name)


# s expretion factory
class s_exp_factory:
    def pretty(tree):
        return json.dumps(tree, indent=4)
    
    def get_type(node):
        return node[0]
    
    def program(tree):
        return ('begin', tree)
    
    def empty_statement():
        return tuple()

    def block_statement(tree):
        return ('begin', tree)

    def string_literal(tree):
        return f'"{tree}"'

    def numeric_literal(tree):
        return int(tree)
    
    def expression_statement(tree):
        return tree
    
    def binary_operator(left, right, operator):
        return (operator, left, right)
    
    def assignment_expression(left, right, operator):
        return (operator, left, right)
    
    def identifier(name):
        return ('Identifier', name)

