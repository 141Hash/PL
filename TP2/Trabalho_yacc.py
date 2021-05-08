import ply.yacc as yacc
import sys
from tokens import tokens


def p_error(p):
    print('Syntax error!')

