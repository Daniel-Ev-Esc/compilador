# Daniel Evaristo Escalera Bonilla 09/03/2024
# parser_.py

import ply.yacc as yacc

from scanner import tokens, lexer

# 0 = int
# 1 = float
# Operaciones = + (suma), - (resta), * (multiplicación), / (división)
# Tabla de consideraciones semánticas

typeDict = {'int':0,'float':1}
operationIndex = {'+':0,'-':1,'*':2,'/':3, '=':4}

tcs = [[[0,0,0,0,0],[1,1,1,1,-1]],[[1,1,1,1,-1],[1,1,1,1,1]]]

poper = []
pilaO = []
pilaType = []
quadQueue = []
resultCounter = 0

def generate_quad_operator(operator, izq, der,resultado):
    global resultCounter
    if resultado == "":
        resultCounter = resultCounter+1
        resultado = "t" + str(resultCounter)
        pilaO.append(resultado)
    quad = [operator,izq,der,resultado]
    print(quad)
    return quad

def p_crear_dir_func(p):
    'crear_dir_func : '
    global dirFunc
    dirFunc = {}

def p_definir_programa(p):
    'definir_programa : '
    dirFunc[p[-1]] = {'name':p[-1],'type':"program"}

    global curr_func
    curr_func = 'global'
    global curr_type
    curr_type = 'void'

    dirFunc[curr_func] = {'name':curr_func,"type":curr_type}

def p_delete_directory(p):
    'delete_directory : '

    global dirFunc

    print (dirFunc)

    del dirFunc

def p_program(p):
    'program : PROGRAM crear_dir_func ID definir_programa PUNTOCOMA vars_opt funcs_opt MAIN body END delete_directory'

def p_vars_opt(p):
    '''vars_opt : vars 
    | empty'''

def p_tabla_variables_global(p):
    'tabla_variables_global : '

    if 'vars' not in dirFunc[curr_func]:
        dirFunc[curr_func]['vars'] = {}

def p_vars(p):
    'vars : VAR tabla_variables_global vars_1'

def p_assign_type_to_vars(p):
    'assign_type_to_vars :'

    for id in dirFunc[curr_func]['vars']:
        if not 'type' in dirFunc[curr_func]['vars'][id]:
            dirFunc[curr_func]['vars'][id] = {'name':id,'type':curr_type}
            
def p_vars_1(p):
    '''vars_1 : id DOSPUNTOS type PUNTOCOMA assign_type_to_vars vars_1
    | empty'''

def p_declaracion_variable(p):
    'declaracion_variable :'

    if not p[-1] in dirFunc[curr_func]['vars']:
        dirFunc[curr_func]['vars'][p[-1]] = {}
    else:
        raise Exception("Declaración Múltiple de variable: '%s'" % p[-1])
    
def p_id(p):
    'id : ID declaracion_variable id_1'

def p_id_1(p):
    '''id_1 : COMA id
    | empty'''

def p_change_curr_type(p):
    'change_curr_type : '

    global curr_type
    curr_type = p[-1]
    
def p_type(p):
    '''type : INT change_curr_type
    | FLOAT change_curr_type'''

def p_funcs_opt(p):
    '''funcs_opt : funcs funcs_opt
    | empty'''

def p_new_function(p):
    'new_function : '
    
    global curr_func
    curr_func = p[-1]

    if not curr_func in dirFunc:
        dirFunc[p[-1]] = {'name':p[-1],'type':curr_type}
    else:
        raise Exception("Declaración Múltiple de función: '%s'" % p[-1])

def p_create_func_var_table(p):
    'create_func_var_table : '
    dirFunc[curr_func]['vars'] = {}

def p_funcs(p):
    'funcs : VOID change_curr_type ID new_function PARENIZQ create_func_var_table params PARENDER BRACKETIZQ vars_opt body BRACKETDER PUNTOCOMA'

def p_params(p):
    '''params : params_1
    | empty'''

def p_parameter_declaration(p):
    'parameter_declaration : '

    if not p[-3] in dirFunc[curr_func]['vars']:
        dirFunc[curr_func]['vars'][p[-3]] = {'name':p[-3],'type':curr_type}
    else:
        raise Exception("Declaración Múltiple de variable: '%s'" % p[-3])

def p_params_1(p):
    '''params_1 : ID DOSPUNTOS type parameter_declaration params_cycle'''

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

def p_push_to_pilaO(p):
    "push_to_pilaO :"
    if(p[-2] == '+' or p[-2] == '-'):
        pilaO.append("".join([p[-2],p[-1]]))
    else:
        pilaO.append(p[-1])

    pilaType.append(dirFunc[curr_func]['vars'][p[-1]]['type'])

def p_push_operator(p):
    "push_operator :"
    poper.append(p[-1])

def p_check_for_assign(p):
    "check_for_assign :"
    if(len(poper) > 0):
        if(poper[-1] == '='):
            operator = poper.pop()
            der = pilaO.pop()
            izq = pilaO.pop()
            generate_quad_operator(operator,izq,"",der)
        elif(poper[-1] == '('):
            poper.pop()

def p_assign(p):
    'assign : ID push_to_pilaO IGUAL push_operator expresion check_for_assign PUNTOCOMA'

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

def p_check_for_expresion(p):
    "check_for_expresion :"
    if(len(poper) > 0):
        if(poper[-1] == '>' or poper[-1]=='<' or poper[-1] == "!="):
            operator = poper.pop()
            der = pilaO.pop()
            izq = pilaO.pop()
            generate_quad_operator(operator,izq,der,"")
        elif(poper[-1] == '('):
            poper.pop()

def p_expresion(p):
    'expresion : exp check_for_expresion expresion_1'

def p_expresion_1(p):
    '''expresion_1 : MENORQUE push_operator exp check_for_expresion
    | MAYORQUE push_operator exp check_for_expresion
    | DIFERENTE push_operator exp check_for_expresion
    | empty'''

def p_check_for_plus_minus(p):
    "check_for_plus_minus :"
    if(len(poper) > 0):
        if(poper[-1] == '+' or poper[-1]=='-'):
            operator = poper.pop()
            der = pilaO.pop()
            izq = pilaO.pop()
            generate_quad_operator(operator,izq,der,"")
        elif(poper[-1] == '('):
            poper.pop()

def p_exp(p):
    'exp : termino check_for_plus_minus exp_1'

def p_exp_1(p):
    '''exp_1 : MINUS push_operator exp
    | PLUS push_operator exp
    | empty'''

def p_check_for_mult_div(p):
    'check_for_mult_div :'
    if(len(poper) > 0):
        if(poper[-1] == '*' or poper[-1]=='/'):
            operator = poper.pop()
            der = pilaO.pop()
            izq = pilaO.pop()
            generate_quad_operator(operator,izq,der,"")
        elif(poper[-1] == '('):
            poper.pop()

def p_termino(p):
    'termino : factor check_for_mult_div termino_1'

def p_termino_1(p):
    '''termino_1 : MULT push_operator termino
    | DIV push_operator termino
    | empty'''

def p_factor(p):
    '''factor : PARENIZQ push_operator expresion PARENDER
    | MINUS factor_1 push_to_pilaO
    | PLUS factor_1 push_to_pilaO
    | factor_1 push_to_pilaO'''

def p_check_variable(p):
    'check_variable :'
    if not p[-1] in dirFunc[curr_func]['vars']:
        raise Exception("Variable no declarada: '%s'" % p[-1])
        
def p_factor_1(p):
    '''factor_1 : ID check_variable
    | cte'''
    p[0] = p[1]

def p_cte(p):
    '''cte : CTE_INT
    | CTE_FLOAT'''
    p[0] = p[1]

def p_empty(p):
    'empty :'
    pass

# Manejo de errores
def p_error(p):
    raise Exception("Error de sintaxis, se encontro elemento inesperado del tipo %s con valor: '%s' en la linea %d" % (p.type, p.value, p.lineno))

parser = yacc.yacc(start='program')

while True:

    poper = []
    pilaO = []
    pilaType = []
    resultCounter = 0

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
        print(poper)
        print(pilaO)
        print(pilaType)

    except ValueError:
        print("Entrada no válida, ingrese un número")
    except Exception as e:
        print("Error:", e)
        
    