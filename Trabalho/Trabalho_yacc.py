import ply.yacc as yacc
import sys
from Trabalho_lex import tokens

def oprecao_aritmetica(p):
    "OPERACAOA : NUM OPERACAO NUM"

def operacao_soma(p):
    "OPERACAO : SOMA"

def operacao_subtracao(p):
    "OPERACAO : SUBTRACAO"

def operacao_multiplicacao(p):
    "OPERACAO : MULTIPLICACAO"

def operacao_divisao(p):
    "OPERACAO : DIVISAO"

def operacao_mod(p):
    "OPERACAO : RESTODI"

def operacao_maior(p):
    "OPERACAO : MAIOR"

def operacao_menor(p):
    "OPERACAO : MENOR"

def operacao_igual(p):
    "OPERACAO : IGUAL"

def operacao_maior_igual(p):
    "OPERACAO : MAIORI"

def operacao_menor_igual(p):
    "OPERACAO : MENORI"

def condicoes():
    "CONDICOES : CONDICAO CAUDAC"

def condicao(p):
    "CONDICAO : OPERACAOA SIMBC OPERACAOA"

def simbolo_conjuncao(p):
    "SIMBC : CONJUNCAO"

def simbolo_disjuncao(p):
    "SIMBC : DISJUNCAO"

def cauda_condicoes(p):
    "CAUDAC : SIMBC OPERACAOA CAUDAC"

def cauda_condicoes_vazio(p):
    "CAUDAC : "

def p_funcao(p):
    "FUNCAO : ID PD ARGS PE"
    

def p_arg_cauda(p):
    "ARGS : ARG CAUDA"

def p_args_vazio(p):
    "ARGS : "

def cauda(p):
    "CAUDA : VIRG ARG CAUDA"

def cauda_vazio(p):
    "CAUDA : "

def arg_id(p):
    "ARG : ID"

def arg_num(p):
    "ARG : NUM"

def p_error(p):
    print('Syntax error!')

