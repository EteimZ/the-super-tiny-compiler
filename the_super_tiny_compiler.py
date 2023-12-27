# The super tiny compiler

# This is an implementation of the-super-tiny-compiler by jamiebuilds in python.
# To learn more about the original version check out his repo: https://github.com/jamiebuilds/the-super-tiny-compiler

# Import all neccesary modules
from dataclasses import dataclass, field
from typing import List, Optional, Union
from abc import ABC, abstractmethod
import types

# This is the token class
# It represents the what is returns from the lexer(tokenizer)
# Each token has a type and the corresponding value.
@dataclass
class Token:
    type: str
    value: str

# This is the node class
# It represents a node in the abstract syntax tree
# Like the token it contains a type and a value.
# With optional parameters
@dataclass
class Node:
    type: str
    value: str
    params: List["Node"] = field(default_factory=list)

    @property
    def name(self):
        return self.value

# This class is the abstract syntax tree
# It consists of nodes connected in a tree structure
# It is the output of the parser
@dataclass
class AST:
    type: str
    body: List["Node"] = field(default_factory=list)

# The visitors job is to visit the nodes during transformation
# of one AST to another
class Visitor(ABC):

    @abstractmethod
    def enter(self):
        pass

# This visitor is used to visit numeric nodes
class NumberVistor(Visitor):
    
    @staticmethod
    def enter(node, parent):
        parent._context.append(Node(type='NumberLiteral', value=node.value))

# This visitor is used to visit string nodes
class StringVistor(Visitor):

    @staticmethod
    def enter(node, parent):
        parent._context.append(Node(type='StringLiteral', value=node.value))

# This visitor is used to visit function calls and other expressions
class ExpressionVisitor:

    @staticmethod
    def enter(node, parent):
        expression = types.SimpleNamespace()
        
        callee = types.SimpleNamespace()
        callee.type = 'Identifier'
        callee.name = node.name

        expression.type = 'CallExpression'
        expression.callee = callee
        expression.arguments = []

        node._context = expression.arguments

        if parent.type != 'CallExpression':
            parent_expression = types.SimpleNamespace()
            parent_expression.type = 'ExpressionStatement'
            parent_expression.expression = expression

        parent._context.append(expression)

# This is tokenizer or the lexer
# It takes in the source code as input
# Then converts it into tokens
def tokenizer(input) -> List[Token]:
    current = 0

    tokens: List[Token] = []

    while current < len(input):
        char = input[current]

        if char == "(":
            tokens.append(Token(type="paren", value="("))

            current += 1

            continue

        if char == ")":
            tokens.append(Token(type="paren", value=")"))

            current += 1

            continue

        if char.isspace():
            current += 1

            continue

        if char.isdigit():
            value = ""

            while char.isdigit():
                value += char
                current += 1
                char = input[current]

            tokens.append(Token(type="number", value=value))

            continue

        if char == '"':
            value = ""

            current += 1
            char = input[current]

            while char != '"':
                value += char
                current += 1
                char = input[current]

            current += 1
            char = input[current]

            tokens.append(Token(type="string", value=value))

            continue

        if char.isalpha():
            value = ""

            while char.isalpha():
                value += char
                current += 1
                char = input[current]

            tokens.append(Token(type="name", value=value))

            continue

        raise Exception(f"I dont know what this character is: {char}")

    return tokens

# This takes in the tokens returned from the tokenizer
# Then returns an Abstract syntax tree
def parser(tokens: List[Token]):
    current = 0

    def walk():
        nonlocal current
        token = tokens[current]

        if token.type == "number":
            current += 1
            return Node(type="NumberLiteral", value=token.value)

        if token.type == "string":
            current += 1
            return Node(type="StringLiteral", value=token.value)
        
        if token.type == "paren" and token.value == "(":
            current += 1
            token = tokens[current]

            node = Node(type="CallExpression", value=token.value)

            current += 1
            token = tokens[current]

            while token.type != "paren" or (token.type == "paren" and token.value != ")"):
                node.params.append(walk())
                token = tokens[current]

            current += 1
            return node

        raise TypeError(token.type)

    ast = AST(type="Program")

    while current < len(tokens):
        ast.body.append(walk())

    return ast

# The traverser job is to visit each and every node in the AST
# Then apply the corresponding visitor method to the node type
def traverser(ast, visitor):

    def traverseArray(array, parent):
        for child in array:
            traverseNode(child, parent)

    def traverseNode(node: Union[Node, AST], parent):

        methods = visitor.get(node.type, None)

        if methods and hasattr(methods, 'enter'):
            methods.enter(node, parent)

        if node.type == 'Program':
            traverseArray(node.body, node)

        elif node.type == 'CallExpression':
            traverseArray(node.params, node)

        elif node.type == 'NumberLiteral' or 'StringLiteral':
            pass

        else:
            raise Exception(node.type)

    traverseNode(ast, None)

# The transformer job is to transform our source AST into the Output AST.
# In this case our input AST is lisp and output is python.
def transformer(ast):

    newAst = AST(type="Program")

    ast._context = newAst.body

    traverser(ast, {"NumberLiteral": NumberVistor, "StringLiteral": StringVistor, "CallExpression": ExpressionVisitor})

    return newAst

# The codeGenerator take in our transformed AST and converts it into source code
def codeGenerator(node):

    if node.type == 'Program':
        lines = list(map(codeGenerator, node.body))
        return '\n'.join(lines)

    elif node.type == 'ExpressionStatement':
        return codeGenerator(node.expression)
    
    elif node.type == 'CallExpression':
        arguments = list(map(codeGenerator, node.arguments))
        return codeGenerator(node.callee) + '(' + ', '.join(arguments) +')'

    elif node.type == 'Identifier':
        return node.name

    elif node.type == 'NumberLiteral':
        return node.value

    elif node.type == 'StringLiteral':
        return '"' + node.value + '"'

    else:
        raise Exception(node.type)

# The compiler
def compiler(program):
    tokens = tokenizer(program)
    ast = parser(tokens)
    newAst = transformer(ast)
    output = codeGenerator(newAst)
    
    return output
