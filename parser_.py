import ply.yacc as yacc

from scanner import tokens

def p_program(p):
    'program : PROGRAM ID PUNTOCOMA vars_opt funcs_opt MAIN body END'
    p[0] = " ".join([p[1],p[2],p[3],p[4],p[5],p[6],p[7],p[8]])

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
    p[0] = "".join([p[1],p[2]])

def p_id_1(p):
    '''id_1 : COMA id
    | empty'''
    if(p[1]):
        p[0] = "".join([p[1],p[2]])
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
    'funcs : VOID ID PARENIZQ params PARENDER BRACKETIZQ vars_opt body BRACKETDER PUNTOCOMA'
    p[0] = " ".join([p[1],p[2],p[3],p[4],p[5], p[6], p[7],p[8],p[9], p[10]])

def p_params(p):
    '''params : params_1
    | empty'''
    if(p[1]):
        p[0] = p[1]
    else:
        p[0] = ""

def p_params_1(p):
    '''params_1 : ID DOSPUNTOS type params_cycle'''
    p[0] = "".join([p[1],p[2],p[3],p[4]])

def p_params_cycle(p):
    '''params_cycle : COMA params_1
    | empty'''
    if(p[1]):
        p[0] = "".join([p[1],p[2]])
    else:
        p[0] = ""

def p_body(p):
    'body : CORCHETEIZQ statement_opt CORCHETEDER'
    p[0] = "".join([p[1],p[2], p[3]])

def p_statement_opt(p):
    '''statement_opt : statement statement_opt
    | empty'''
    if(p[1]):
        p[0] = " ".join([p[1],p[2]])
    else:
        p[0] = ""
def p_statement(p):
    '''statement : assign
    | condition 
    | cycle
    | f_call
    | print'''
    p[0] = p[1]

def p_assign(p):
    'assign : exp IGUAL expresion'
    p[0] = "".join([p[1],p[2],p[3]])

def p_condition(p):
    'condition : IF PARENIZQ expresion PARENDER body else'
    p[0] = "".join([p[1],p[2],p[3],p[4],p[5],p[6]])

def p_else(p):
    '''else : ELSE body
    | empty'''
    if(p[1]):
        p[0] = "".join([p[1],p[2]])
    else:
        p[0] = ""

def p_cycle(p):
    'cycle : DO body WHILE PARENIZQ expresion PARENDER'
    p[0] = " ".join([p[1],p[2],p[3],p[4],p[5],p[6]])

def p_f_call(p):
    'f_call : ID PARENIZQ expresion_opt PARENDER'
    p[0] = "".join([p[1],p[2],p[3],p[4]])

def p_print(p):
    'print : PRINT PARENIZQ printable PARENDER'
    p[0] = "".join([p[1],p[2],p[3],p[4]])

def p_printable(p):
    '''printable : CTE_STRING printable_1
    | expresion printable_1'''
    p[0] = "".join([p[1],p[2]])

def p_printable_1(p):
    '''printable_1 : COMA printable
    | empty'''
    if(p[1]):
        p[0] = "".join([p[1],p[2]])
    else:
        p[0] = ""

def p_expresion_opt(p):
    '''expresion_opt : expresion expresion_cycle
    | empty'''
    if(p[1]):
        p[0] = "".join([p[1],p[2]])
    else:
        p[0] = ""

def p_expresion_cycle(p):
    '''expresion_cycle : COMA expresion_opt
    | empty'''
    if(p[1]):
        p[0] = "".join([p[1],p[2]])
    else:
        p[0] = ""

def p_expresion(p):
    'expresion : exp expresion_1'
    p[0] = "".join([p[1],p[2]])

def p_expresion_1(p):
    '''expresion_1 : MENORQUE exp
    | MAYORQUE exp
    | EXCLAMACION IGUAL exp
    | empty'''
    if(p[1]):
        if(len(p) > 3):
            p[0] = "".join([p[1],p[2],p[3]])
        else:
            p[0] = "".join([p[1],p[2]])
    else:
        p[0] = ""

def p_exp(p):
    'exp : termino exp_1'
    p[0] = "".join([p[1],p[2]])

def p_exp_1(p):
    '''exp_1 : MINUS exp
    | PLUS exp
    | empty'''
    if(p[1]):
        p[0] = "".join([p[1],p[2]])
    else:
        p[0] = ""

def p_termino(p):
    'termino : factor termino_1'
    p[0] = "".join([p[1],p[2]])

def p_termino_1(p):
    '''termino_1 : MULT termino
    | DIV termino
    | empty'''
    if(p[1]):
        p[0] = "".join([p[1],p[2]])
    else:
        p[0] = ""

def p_factor(p):
    '''factor : PARENIZQ expresion PARENDER
    | MINUS factor_1
    | PLUS factor_1
    | factor_1'''
    if(len(p) > 3):
        p[0] = "".join([p[1],p[2],p[3]])
    elif(len(p) > 2):
        p[0] = "".join([p[1],p[2]])
    else:
        p[0] = p[1]
        
def p_factor_1(p):
    '''factor_1 : ID
    | cte'''
    p[0] = p[1]

def p_cte(p):
    '''cte : CTE_INT
    | CTE_FLOAT'''
    p[0] = p[1]



def p_empty(p):
    'empty :'
    pass

# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input!")

# Build the parser
parser = yacc.yacc(start='program')

s = ('program helloworld; var counter, indice, patito:int; void imprimir(numero:int, numerofloat:float)[var resultado:int;{placeholder=placeholder if(mayor>menor){mayor=9} do{i=i+1}while(i<10) imprimir(9.0) print("Esto es un string","Esto tambien",estono,7) }]; void leer()[{ igual = 2/2.8+2 }]; main {if(mayor>menor){mayor=9}else{menor=0}} end')
result = parser.parse(s)
print(result)