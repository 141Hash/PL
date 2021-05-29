import ply.yacc as yacc
import sys
from Trabalho_lex import tokens
from Trabalho_lex import literals


# Definição da Gramática:
#
# Programa : BEGD '[' Declaracoes ']' BEGI '[' Instrucoes ']'
#
# Declaracoes : Declaracoes Declaracao
# Declaracoes : "
# Declaracao : INT ID '=' OPERACAO ';'
# Declaracao : INT ID '[' NUM ']' ';'
# Declaracao : INT ID '[' NUM ']' '[' NUM ']' ';'
# Declaracao : INT ID ';'
#
# Instrucoes : Instrucoes Instrucao
# Instrucoes : 
# Instrucao : Atribuicao ';'
# Instrucao : READ '(' ID ')' ';'
# Instrucao : WRITE '(' OPERACAO ')' ';'
# Instrucao : PRINT '(' STRING ')' ';'
# Instrucao : IF '(' Logica ')' '{' Instrucoes '}'
# Instrucao : IF '(' Logica ')' '{' Instrucoes '}' ELSE '{' Instrucoes '}'
# Instrucao : FOR '(' Atribuicao ';' Logica ';' Atribuicao ')' '{' Instrucoes '}'
# Instrucao : WHILE '(' Logica ')' '{' Instrucoes '}'
# Instrucao : REPEAT '{' Instrucoes '}' UNTIL '(' Logica ')'
#
# Atribuicao : ID '=' OPERACAO
# Atribuicao : ID '[' OPERACAO ']' '=' OPERACAO
# Atribuicao : ID '[' OPERACAO ']' '[' OPERACAO ']' '=' OPERACAO
#
# Logica : Logica AND COND
# Logica : Logica OR COND
# Logica : NOT COND
# Logica : COND
#
# COND : OPERACAO IGUAL OPERACAO
# COND : OPERACAO DIF OPERACAO
# COND : OPERACAO '>' OPERACAO
# COND : OPERACAO '<' OPERACAO
# COND : OPERACAO MAIORI OPERACAO
# COND : OPERACAO MENORI OPERACAO
# COND : OPERACAO
#
# OPERACAO : OPERACAO '+' TERMO
# OPERACAO : OPERACAO '-' TERMO
# OPERACAO : TERMO
#  
# TERMO : TERMO '*' FACTOR
# TERMO : TERMO '/' FACTOR
# TERMO : TERMO '%' FACTOR
# TERMO : FACTOR
#
# FACTOR : ID
# FACTOR : NUM
# FACTOR : '(' OPERACAO ')'
# FACTOR : ID '[' OPERACAO ']'
# FACTOR : ID '[' OPERACAO ']' '[' OPERACAO ']'

def p_programa(p):
    "Programa : BEGD '[' Declaracoes ']' BEGI '[' Instrucoes ']'"
    p[0] = p[3] + 'start\n' + p[7] + 'stop'
    
def p_declaracoes(p):
    "Declaracoes : Declaracoes Declaracao"
    p[0] = p[1] + p[2]

def p_declaracoes_empty(p):
    "Declaracoes : "
    p[0] = ""

def p_declaracao_num(p):
    "Declaracao : INT ID '=' OPERACAO ';'"
    p[0] = p[4]
    p.parser.registos[p[2]] = ['int', p.parser.gp]
    p.parser.gp += 1

def p_declaracao_array(p):
    "Declaracao : INT ID '[' NUM ']' ';'"
    p[0] = "pushn " + p[4] + "\n"
    p.parser.registos[p[2]] = ['int', p.parser.gp]
    p.parser.gp += int(p[4])

def p_declaracao_matrix(p):
    "Declaracao : INT ID '[' NUM ']' '[' NUM ']' ';'"
    p[0] = "pushn " + str(int(p[4]) * int(p[7])) + "\n"
    p.parser.registos[p[2]] = ['int', p.parser.gp, int(p[7])]
    p.parser.gp += int(p[4]) * int(p[7])

def p_declaracao_unica(p):
    "Declaracao : INT ID ';'"
    p[0] = 'pushi 0' + "\n"
    p.parser.registos[p[2]] = ['int', p.parser.gp]
    p.parser.gp += 1

def p_instrucoes(p):
    "Instrucoes : Instrucoes Instrucao"
    p[0] = p[1] + p[2]

def p_instrucoes_empty(p):
    "Instrucoes : "
    p[0] = ""

def p_instrucao_atrib(p):
    "Instrucao : Atribuicao ';'"
    p[0] = p[1]

def p_atribuicao(p):
    "Atribuicao : ID '=' OPERACAO"
    offset = p.parser.registos[p[1]][1]
    p[0] = p[3] + "storeg " + str(offset) + "\n"

def p_atribuicao_array(p):
    "Atribuicao : ID '[' OPERACAO ']' '=' OPERACAO"
    offset = p.parser.registos[p[1]][1]
    p[0] = "pushgp\n" + "pushi " + str(offset) + "\n" + "padd\n" + p[3] + p[6] + "storen\n"

def p_atribuicao_matrix(p):
    "Atribuicao : ID '[' OPERACAO ']' '[' OPERACAO ']' '=' OPERACAO"
    offset = p.parser.registos[p[1]][1]
    coluna = p.parser.registos[p[1]][2]
    p[0] = "pushgp\n" + "pushi " + str(offset) + "\n" + "padd\n" + p[6] + p[3] + "pushi " + str(coluna) + "\n" + "mul\nadd\n" + p[9] + "storen\n"

def p_instrucao_read(p):
    "Instrucao : READ '(' ID ')' ';'"
    offset = p.parser.registos[p[3]][1]
    p[0] = 'read ' + "\n" + 'atoi \n' + "storeg " + str(offset) + "\n"

def p_instrucao_write(p):
    "Instrucao : WRITE '(' OPERACAO ')' ';'"
    p[0] = p[3] + 'writei ' + "\n"

def p_instrucao_print(p):
    "Instrucao : PRINT '(' STRING ')' ';'"
    p[0] = "pushs " + p[3] + '\nwrites ' + "\n" 

def p_instrucao_if(p):
    "Instrucao : IF '(' Logica ')' '{' Instrucoes '}'"
    p.parser.if_count += 1
    p[0] = p[3] + "jz fimif" + str(p.parser.if_count) + "\n" + p[6] + "fimif" + str(p.parser.if_count) + ":\n"

def p_instrucao_ifelse(p):
    "Instrucao : IF '(' Logica ')' '{' Instrucoes '}' ELSE '{' Instrucoes '}'"
    p.parser.if_count += 1
    number = str(p.parser.if_count) 
    p[0] = p[3] + "jz else" + number + "\n" + p[6] + "jump fimif"+ number + "\n" +"else" + number + ":\n" + p[10] + "fimif" + number + ":\n"

def p_instrucao_for(p):
    "Instrucao : FOR '(' Atribuicao ';' Logica ';' Atribuicao ')' '{' Instrucoes '}'"
    p.parser.for_count += 1
    number = str(p.parser.for_count) 
    p[0] = p[3] + "inicfor" + number + ":\n" + p[5] + "jz fimfor" + number + "\n" + p[10] + p[7] + "jump inicfor" + number + "\n" + "fimfor" + number + ":\n"

def p_instrucao_while(p):
    "Instrucao : WHILE '(' Logica ')' '{' Instrucoes '}'"
    p.parser.while_count += 1
    number = str(p.parser.while_count)
    p[0] = "inicwhile" + number + ":\n" + p[3] + "jz fimwhile" + number + "\n" + p[6] + "jump inicwhile" + number + "\n" + "fimwhile" + number + ":\n"

def p_instrucao_repeat(p):
    "Instrucao : REPEAT '{' Instrucoes '}' UNTIL '(' Logica ')'"
    p.parser.repeat_count += 1
    number = str(p.parser.repeat_count)
    p[0] = "inicrepeat" + number + ":\n" + p[7] + "jz fimrepeat" + number + "\n" + p[3] + "jump inicrepeat" + number + "\n" + "fimrepeat" + number + ":\n"

def p_logica_and(p):
    "Logica : Logica AND COND"
    p[0] = p[1] + p[3] + "mul" + "\n"

def p_logica_or(p):
    "Logica : Logica OR COND"
    p[0] = p[1] + p[3] + "mul" + "\n" + p[1] + p[3]+ "add \n" + "sub \n"

def p_logica_not(p):
    "Logica : NOT COND"
    p[0] = p[2] + "not \n"

def p_logica_cond(p):
    "Logica : COND"
    p[0] = p[1]

def p_cond_equal(p):
    "COND : OPERACAO IGUAL OPERACAO"
    p[0] = p[1] + p[3] + "equal \n"

def p_cond_dif(p):
    "COND : OPERACAO DIF OPERACAO"
    p[0] = p[1] + p[3] + "equal \n" + "not \n"

def p_cond_maior(p):
    "COND : OPERACAO '>' OPERACAO"
    p[0] = p[1] + p[3] + "sup \n"

def p_cond_menor(p):
    "COND : OPERACAO '<' OPERACAO"
    p[0] = p[1] + p[3] + "inf \n"

def p_cond_maiorEq(p):
    "COND : OPERACAO MAIORI OPERACAO"
    p[0] = p[1] + p[3] + "supeq \n"

def p_cond_menorEq(p):
    "COND : OPERACAO MENORI OPERACAO"
    p[0] = p[1] + p[3] + "infeq \n"

def p_cond_operacao(p):
    "COND : OPERACAO"
    p[0] = p[1]

def p_operacao_add(p):
    "OPERACAO : OPERACAO '+' TERMO"
    p[0] = p[1] + p[3] + 'add' + '\n'

def p_operacao_sub(p):
    "OPERACAO : OPERACAO '-' TERMO"
    p[0] = p[1] + p[3] + 'sub' + '\n'
1
def p_operacao_term(p):
    "OPERACAO : TERMO"
    p[0] = p[1]

def p_termo_mul(p):
    "TERMO : TERMO '*' FACTOR"
    p[0] = p[1] + p[3] + 'mul' + '\n'

def p_termo_div(p):
    "TERMO : TERMO '/' FACTOR"
    p[0] = p[1] + p[3] + 'div' + '\n'

def p_termo_mod(p):
    "TERMO : TERMO '%' FACTOR"
    p[0] = p[1] + p[3] + 'mod' + '\n'

def p_termo_factor(p):
    "TERMO : FACTOR"
    p[0] = p[1]

def p_factor_id(p):
    "FACTOR : ID"
    offset = p.parser.registos[p[1]][1]
    p[0] = 'pushg ' + str(offset) + '\n'

def p_factor_number(p):
    "FACTOR : NUM"
    p[0] = 'pushi ' + p[1] + '\n'

def p_factor_group(p):
    "FACTOR : '(' OPERACAO ')'"
    p[0] = p[2]

def p_factor_array(p):
    "FACTOR : ID '[' OPERACAO ']'"
    offset = p.parser.registos[p[1]][1]
    p[0] = "pushgp\n" + "pushi " + str(offset) + "\n" + "padd\n" + p[3] + "loadn\n"

def p_factor_matrix(p):
    "FACTOR : ID '[' OPERACAO ']' '[' OPERACAO ']'"
    offset = p.parser.registos[p[1]][1]
    coluna = p.parser.registos[p[1]][2]
    p[0] = "pushgp\n" + "pushi " + str(offset) + "\n" + "padd\n" + p[6] + p[3] + "pushi " + str(coluna) + "\n" + "mul\nadd\n" + "loadn\n"

def p_error(p):
    print('Syntax error! ', p)

parser = yacc.yacc()

parser.registos = {}
parser.gp = 0
parser.if_count = 0
parser.for_count = 0
parser.while_count = 0
parser.repeat_count = 0

q = 0

while q == 0:
    inputFile = input('File to read >> ')
    try:
        file = open(inputFile, 'r')
        q = 1
    except OSError:
        print('Ficheiro inválido')

fileOutput = input('Output file >> ')
fileOut = open(fileOutput, 'w+')

fileData = file.read()
result = parser.parse(fileData)
fileOut.write(result)

file.close()
fileOut.close()

