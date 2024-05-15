# Daniel Evaristo Escalera Bonilla 09/03/2024
# parser_.py

import ply.yacc as yacc

from scanner import tokens, lexer

# 0 = int
# 1 = float
# Operaciones = + (suma), - (resta), * (multiplicación), / (división)
# Tabla de consideraciones semánticas

typeDict = {'int':0,'float':1}
operationIndex = {'+':0,'-':1,'*':2,'/':3}

tcs = [[[0,0,0,0],[1,1,1,1]],[[1,1,1,1],[1,1,1,1]]]

def p_action_1(p):
    'action_1 : '
    global dirFunc
    dirFunc = {}

def p_action_2(p):
    'action_2 : '
    dirFunc[p[-1]] = {'name':p[-1],'type':"program"}

    global curr_func
    curr_func = 'global'
    global curr_type
    curr_type = 'void'

    dirFunc[curr_func] = {'name':curr_func,"type":curr_type}

def p_action_3(p):
    'action_3 : '

    if 'vars' not in dirFunc[curr_func]:
        dirFunc[curr_func]['vars'] = {}

def p_action_4(p):
    'action_4 :'

    if not p[-1] in dirFunc[curr_func]['vars']:
        dirFunc[curr_func]['vars'][p[-1]] = {}
    else:
        raise Exception("Declaración Múltiple de variable: '%s'" % p[-1])

def p_action_5(p):
    'action_5 : '

    global curr_type
    curr_type = p[-1]

def p_action_aux_5(p):
    'action_aux_5 :'

    for id in dirFunc[curr_func]['vars']:
        if not 'type' in dirFunc[curr_func]['vars'][id]:
            dirFunc[curr_func]['vars'][id] = {'name':id,'type':curr_type}

def p_action_6(p):
    'action_6 : '

    global dirFunc

    print (dirFunc)

    del dirFunc

def p_action_8(p):
    'action_8 : '
    global curr_type
    curr_type = p[-1]

def p_action_9(p):
    'action_9 : '
    
    global curr_func
    curr_func = p[-1]

    if not curr_func in dirFunc:
        dirFunc[p[-1]] = {'name':p[-1],'type':curr_type}
    else:
        raise Exception("Declaración Múltiple de función: '%s'" % p[-1])

def p_action_10(p):
    'action_10 : '
    dirFunc[curr_func]['vars'] = {}

def p_action_11(p):
    'action_11 : '

    if not p[-3] in dirFunc[curr_func]['vars']:
        dirFunc[curr_func]['vars'][p[-3]] = {'name':p[-3],'type':curr_type}
    else:
        raise Exception("Declaración Múltiple de variable: '%s'" % p[-3])

def p_action_12(p):
    'action_12 : '
    # print(dirFunc[curr_func])
    # del dirFunc[curr_func]


def p_program(p):
    'program : PROGRAM action_1 ID action_2 PUNTOCOMA vars_opt funcs_opt MAIN body END action_6'

def p_vars_opt(p):
    '''vars_opt : vars 
    | empty'''

def p_vars(p):
    'vars : VAR action_3 vars_1'

def p_vars_1(p):
    '''vars_1 : id DOSPUNTOS type PUNTOCOMA action_aux_5 vars_1
    | empty'''

def p_id(p):
    'id : ID action_4 id_1'

def p_id_1(p):
    '''id_1 : COMA id
    | empty'''

def p_type(p):
    '''type : INT action_5
    | FLOAT action_5'''

def p_funcs_opt(p):
    '''funcs_opt : funcs funcs_opt
    | empty'''

def p_funcs(p):
    'funcs : VOID action_8 ID action_9 PARENIZQ action_10 params PARENDER BRACKETIZQ vars_opt body BRACKETDER PUNTOCOMA action_12'

def p_params(p):
    '''params : params_1
    | empty'''

def p_params_1(p):
    '''params_1 : ID DOSPUNTOS type action_11 params_cycle'''

def p_params_cycle(p):
    '''params_cycle : COMA params_1
    | empty'''

def p_body(p):
    'body : CORCHETEIZQ statement_opt CORCHETEDER'

def p_statement_opt(p):
    '''statement_opt : statement statement_opt
    | empty'''

def p_statement(p):
    '''statement : assign
    | condition 
    | cycle
    | f_call
    | print'''

def p_assign(p):
    'assign : exp IGUAL expresion PUNTOCOMA'

def p_condition(p):
    'condition : IF PARENIZQ expresion PARENDER body else PUNTOCOMA'

def p_else(p):
    '''else : ELSE body
    | empty'''

def p_cycle(p):
    'cycle : DO body WHILE PARENIZQ expresion PARENDER PUNTOCOMA'

def p_f_call(p):
    'f_call : ID PARENIZQ expresion_opt PARENDER PUNTOCOMA'

def p_print(p):
    'print : PRINT PARENIZQ printable PARENDER PUNTOCOMA'

def p_printable(p):
    '''printable : CTE_STRING printable_1
    | expresion printable_1'''

def p_printable_1(p):
    '''printable_1 : COMA printable
    | empty'''

def p_expresion_opt(p):
    '''expresion_opt : expresion expresion_cycle
    | empty'''

def p_expresion_cycle(p):
    '''expresion_cycle : COMA expresion_opt
    | empty'''

def p_expresion(p):
    'expresion : exp expresion_1'

def p_expresion_1(p):
    '''expresion_1 : MENORQUE exp
    | MAYORQUE exp
    | EXCLAMACION IGUAL exp
    | empty'''

def p_exp(p):
    'exp : termino exp_1'

def p_exp_1(p):
    '''exp_1 : MINUS exp
    | PLUS exp
    | empty'''

def p_termino(p):
    'termino : factor termino_1'

def p_termino_1(p):
    '''termino_1 : MULT termino
    | DIV termino
    | empty'''

def p_factor(p):
    '''factor : PARENIZQ expresion PARENDER
    | MINUS factor_1
    | PLUS factor_1
    | factor_1'''
        
def p_factor_1(p):
    '''factor_1 : ID
    | cte'''

def p_cte(p):
    '''cte : CTE_INT
    | CTE_FLOAT'''

def p_empty(p):
    'empty :'
    pass

# Manejo de errores
def p_error(p):
    raise Exception("Error de sintaxis, se encontro elemento inesperado del tipo %s con valor: '%s' en la linea %d" % (p.type, p.value, p.lineno))

parser = yacc.yacc(start='program')

while True:

    try :
        input_ = int(input('''Seleccione un archivo de prueba o ingrese su propio texto en el archivo personalizado, ingrese 0 o cualquier elemento que no esté en la lista para salir:
1. test_1 (Completo) 
2. test_2 (Error léxico) 
3. test_3 (Error sintáctico)
4. test_4 (Simple)
5. test_5 (Multiples parametros, statements, expresiones)
6. test_6 (Multiple declaración de parámetros)
7. test_7 (Multiple declaración de funciones)
8. test_8 (Multiple declaración de variables)
9. Custom (Coloque su texto de prueba en el archivo custom.txt)
0. Salir\n'''))
        
        lexer.lineno = 1

        if(input_ == 1):
            with open('test_1.txt','r') as archivo:
                s = archivo.read()
        elif(input_ == 2):
            with open('test_2.txt','r') as archivo:
                s = archivo.read()
        elif(input_ == 3):
            with open('test_3.txt','r') as archivo:
                s = archivo.read()
        elif(input_ == 4):
            with open('test_4.txt','r') as archivo:
                s = archivo.read()
        elif(input_ == 5):
            with open('test_5.txt','r') as archivo:
                s = archivo.read()
        elif(input_ == 6):
            with open('test_6.txt','r') as archivo:
                s = archivo.read()
        elif(input_ == 7):
            with open('test_7.txt','r') as archivo:
                s = archivo.read()
        elif(input_ == 8):
            with open('test_8.txt','r') as archivo:
                s = archivo.read()
        elif(input_ == 9):
            with open('custom.txt','r') as archivo:
                s = archivo.read()
        else:
            break
        result = parser.parse(s)

    except ValueError:
        print("Entrada no válida, ingrese un número")
    except Exception as e:
        print("Error:", e)
        
    