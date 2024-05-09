import ply.yacc as yacc

from scanner import tokens

def p_program(p):
    'program : PROGRAM ID PUNTOCOMA vars_opt funcs_opt MAIN END'
    p[0] = " ".join([p[1],p[2],p[3],p[4],p[5],p[6],p[7]])

def p_vars_opt(p):
    '''vars_opt : vars 
    | empty'''
    if(p[1]):
        p[0] = p[1]
    else:
        p[0] = ""

def p_vars(p):
    'vars : VAR vars_1'
    p[0] = " ".join([p[1],p[2]])

def p_vars_1(p):
    '''vars_1 : id DOSPUNTOS type PUNTOCOMA 
    | empty'''
    if(p[1]):
        p[0] = " ".join([p[1],p[2],p[3],p[4]])
    else:
        p[0] = ""

def p_id(p):
    'id : ID id_1'
    p[0] = " ".join([p[1],p[2]])

def p_id_1(p):
    '''id_1 : COMA id
    | empty'''
    if(p[1]):
        p[0] = " ".join([p[1],p[2]])
    else:
        p[0] = ""

def p_type(p):
    '''type : INT
    | FLOAT'''
    p[0] = p[1]

def p_funcs_opt(p):
    '''funcs_opt : funcs funcs_opt
    | empty'''
    if(p[1]):
        p[0] = " ".join([p[1],p[2]])
    else:
        p[0] = ""

def p_funcs(p):
    'funcs : VOID ID PARENIZQ params PARENDER PUNTOCOMA'
    p[0] = " ".join([p[1],p[2],p[3],p[4],p[5], p[6]])

def p_params(p):
    '''params : params_1
    | empty'''
    if(p[1]):
        p[0] = p[1]
    else:
        p[0] = ""

def p_params_1(p):
    '''params_1 : ID DOSPUNTOS type params_cycle'''
    p[0] = " ".join([p[1],p[2],p[3],p[4]])

def p_params_cycle(p):
    '''params_cycle : COMA params_1
    | empty'''
    if(p[1]):
        p[0] = " ".join([p[1],p[2]])
    else:
        p[0] = ""
    
def p_empty(p):
    'empty :'
    pass

# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input!")

# Build the parser
parser = yacc.yacc(start='program')

s = ('program helloworld; var counter, indice, patito:int; void imprimir(numero:int, numerofloat:float); void leer(); main end')
result = parser.parse(s)
print(result)