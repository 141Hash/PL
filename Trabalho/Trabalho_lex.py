import ply.lex as lex
import sys

tokens = [
    'BEGD',
    'BEGI',
    'READ',
    'WRITE',
    'ID',
    'INT',
    'NUM',
    'IGUAL',
    'DIF',
    'MAIORI',
    'MENORI',
    'AND',
    'OR',
    'NOT',
    'IF',
    'ELSE',
    'FOR',
    'PRINT',
    'WHILE',
    'REPEAT',
    'UNTIL',
    'STRING'
]

literals = ['+', '-', '*', '/', '=', '{', '}', '(', ')', '>', '<', ',', ';', '%', '[', ']']

def t_INT(t):
    r'int'
    return t

def t_NUM(t):
    r'\d+'
    return t

def t_BEGD(t):
    r'BEGD'
    return t

def t_BEGI(t):
     r'BEGI'
     return t

def t_READ(t):
     r'READ'
     return t

def t_WRITE(t):
     r'WRITE'
     return t

def t_PRINT(t):
     r'PRINT'
     return t

def t_WHILE(t):
     r'WHILE'
     return t

def t_REPEAT(t):
     r'REPEAT'
     return t

def t_UNTIL(t):
     r'UNTIL'
     return t

def t_IF(t):
     r'IF'
     return t

def t_ELSE(t):
     r'ELSE'
     return t
     
def t_FOR(t):
    r'FOR'
    return t

def t_IGUAL(t):
     r'=='
     return t

def t_DIF(t):
     r"!="
     return t

def t_MAIORI(t):
     r'>='
     return t

def t_MENORI(t):
    r'<='
    return t

def t_AND(t): 
    r'&&'
    return t

def t_OR(t):
     r'\|\|'
     return t

def t_NOT(t): 
    r'!'
    return t

def t_STRING(t): 
    r'"(.*?)"'
    return t

def t_ID(t):
    r'\w+'
    return t

t_ignore = ' \r\n\t'

def t_error(t):
    print('Illegal character: %s', t.value[0])
    t.lexer.skip(1)

lexer = lex.lex()





