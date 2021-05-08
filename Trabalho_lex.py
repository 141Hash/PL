import ply.lex as lex

tokens = (
    'ID',
    'INT',
    'NUM',
    'PV',
    'PD',
    'PE',
    'MAIOR',
    'IGUAL',
    'MENOR',
    'MAIORI',
    'MENORI',
    'SOMA',
    'SUBTRACAO',
    'MULTIPLICACAO',
    'DIVISAO',
    'CONJUNCAO',
    'DISJUNCAO',
    'RESTODI'
)

t_ID = r'\w+'
t_INT = r'Int'
t_NUM = r'\d+'
t_PV = r';'
t_PD = r'\)'
t_PE = r'\('
t_MAIOR = r'>'
t_MENOR = r'<'
t_IGUAL = r'=='
t_MAIORI = r'>='
t_MENORI = r'<='
t_SOMA = r'\+'
t_SUBTRACAO = r'-'
t_MULTIPLICACAO = r'\*'
t_DIVISAO = r'/'
t_CONJUNCAO = r'&&'
t_DISJUNCAO = r'\|\|'
t_RESTODI = r'%'

t_ignore = ' \r\n\t'

def t_error(t):
    print('Illegal character: %s', t.value[0])

lexer = lex.lex()



