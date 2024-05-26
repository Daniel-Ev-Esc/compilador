# Daniel Evaristo Escalera Bonilla 09/03/2024
# parser_.py

import ply.yacc as yacc

from scanner import tokens, lexer

poper = []
pilaO = []
pilaType = []
pilaSalto = []
quadQueue = []
quadCounter = 1
tempCounter = 0
intCounter = 0
floatCounter = 0
constIntCounter = 1
constFloatCounter = 0
constVarTable = {'0':{"dir":15000, "value":0}}

typeDict = {"int":0,"float":1}
operationIndex = {"+":0,"-":1,"*":2,"/":3, "=":4, ">":5, "<":6,"!=":7, "print":8, "Goto":9, "GotoF":10, "GotoT":11}

# ---------- Funciones Auxiliares ----------

def get_dir(type_):
    # Enteros: 10000 - 39999
    # Flotantes: 40000 - 79999
    # Temporales: 80000 - 149999 

    if type_ == "int":
        global intCounter
        if 1000 + intCounter + 1 < 4000:
            direccion = 1000 + intCounter
            intCounter = intCounter+1
        else:
            raise Exception("Memoria insuficiente")
    elif type_ == "float":
        global floatCounter
        if 4000 + floatCounter + 1 < 8000:
            direccion = 4000 + floatCounter
            floatCounter = floatCounter+1
        else:
            raise Exception("Memoria insuficiente")
    elif type_ == "temp":
        global tempCounter

        if 8000 + tempCounter + 1 < 15000:
            direccion = 8000 + tempCounter
        else:
            raise Exception("Memoria insuficiente")
    elif type_ == "const_int":
        global constIntCounter

        if 15000 + constIntCounter + 1 < 20000:
            direccion = 15000 + constIntCounter
            constIntCounter = constIntCounter + 1
        else:
            raise Exception("Memoria insuficiente")
    elif type_ == "const_float":
        global constFloatCounter

        if 20000 + constFloatCounter + 1 < 25000:
            direccion = 20000 + constFloatCounter
            constFloatCounter = constFloatCounter + 1
        else:
            raise Exception("Memoria insuficiente")
        
    return direccion

def fill_goto(i, obj):
    quadQueue[i-1][3] = obj

def check_semantics(operator, linea):

    tcs = [[["int","int","int","int","int","int","int","int"],["float","float","float","float","ERROR","int","int","int"]],[["float","float","float","float","ERROR","int","int","int"],["float","float","float","float","float","int","int","int"]]]

    type_1 = pilaType.pop()
    type_2 = pilaType.pop()

    resultType = tcs[typeDict[type_1]][typeDict[type_2]][operationIndex[operator]]# tcs[typeDict[type_1]][typeDict[typeDict[type_1]][operationIndex[operator]]]

    if(resultType == "ERROR"):
        raise Exception("Tipos no compatibles para operación %s y %s en la línea: %d" % (type_1,type_2, linea))
    elif(operator != "="):
        pilaType.append(resultType)

def generate_quad_operator(operator, izq, der,resultado):
    global tempCounter, quadCounter
    if resultado == "":
        resultado =  get_dir("temp")
        tempCounter = tempCounter+1
        pilaO.append(resultado)

    quad = [operationIndex[operator],izq,der,resultado]
    quadQueue.append(quad)
    quadCounter = quadCounter + 1
    return quad

# ---------- Reglas y acciones ----------

# -------- Program --------

def p_crear_dir_func(p):
    "crear_dir_func : "
    global dirFunc
    dirFunc = {}

def p_definir_programa(p):
    "definir_programa : "
    dirFunc[p[-1]] = {"type":"program"}

    global curr_func
    curr_func = "global"
    global curr_type
    curr_type = "void"

    dirFunc[curr_func] = {"type":curr_type}

def p_delete_directory(p):
    "delete_directory : "

    global dirFunc

    with open("result.txt","w") as f:
        print(dirFunc, file=f)
        print("$", file=f)
        print(constVarTable, file=f)
        print("$", file=f)
        for x in quadQueue:
            print(x, '&', file=f)

    del dirFunc

def p_return_to_global(p):
    "return_to_global : "

    global curr_func
    curr_func = "global"

def p_program(p):
    "program : PROGRAM crear_dir_func ID definir_programa PUNTOCOMA vars_opt funcs_opt MAIN return_to_global body END delete_directory"

# -------- Variables --------

def p_vars_opt(p):
    '''vars_opt : vars 
    | empty'''

def p_tabla_variables_global(p):
    "tabla_variables_global : "

    if "vars" not in dirFunc[curr_func]:
        dirFunc[curr_func]["vars"] = {}

def p_vars(p):
    "vars : VAR tabla_variables_global vars_1"

def p_assign_type_to_vars(p):
    "assign_type_to_vars :"

    for id in dirFunc[curr_func]["vars"]:
        if not "type" in dirFunc[curr_func]["vars"][id]:
            direccion = get_dir(curr_type)
            dirFunc[curr_func]["vars"][id]["dir"] = direccion
            dirFunc[curr_func]["vars"][id]["type"] = curr_type
            
def p_vars_1(p):
    '''vars_1 : id DOSPUNTOS type PUNTOCOMA assign_type_to_vars vars_1
    | empty'''

def p_declaracion_variable(p):
    "declaracion_variable :"

    if not p[-1] in dirFunc[curr_func]["vars"]:
        dirFunc[curr_func]["vars"][p[-1]] = {}
    else:
        raise Exception("Declaración Múltiple de variable: '%s' en la línea: %d" % (p[-1], lexer.lineno))
    
def p_id(p):
    "id : ID declaracion_variable id_1"

def p_id_1(p):
    '''id_1 : COMA id
    | empty'''

def p_change_curr_type(p):
    "change_curr_type : "

    global curr_type
    curr_type = p[-1]
    
def p_type(p):
    '''type : INT change_curr_type
    | FLOAT change_curr_type'''

# -------- Funciones --------
def p_funcs_opt(p):
    '''funcs_opt : funcs funcs_opt
    | empty'''

def p_new_function(p):
    "new_function : "
    
    global curr_func
    curr_func = p[-1]

    if not curr_func in dirFunc:
        dirFunc[p[-1]] = {"type":curr_type}
    else:
        raise Exception("Declaración Múltiple de función: '%s' en la línea: %d" % (p[-1], lexer.lineno))

def p_create_func_var_table(p):
    "create_func_var_table : "
    dirFunc[curr_func]["vars"] = {}

def p_funcs(p):
    "funcs : VOID change_curr_type ID new_function PARENIZQ create_func_var_table params PARENDER BRACKETIZQ vars_opt body BRACKETDER PUNTOCOMA"

def p_params(p):
    '''params : params_1
    | empty'''

def p_parameter_declaration(p):
    "parameter_declaration : "

    if not p[-3] in dirFunc[curr_func]["vars"]:
        direccion = get_dir(curr_type)
        dirFunc[curr_func]["vars"][p[-3]] = {"type":curr_type, "dir":direccion}
    else:
        raise Exception("Declaración Múltiple de variable: '%s' en la línea: %d" % (p[-3],lexer.lineno))

def p_params_1(p):
    '''params_1 : ID DOSPUNTOS type parameter_declaration params_cycle'''

def p_params_cycle(p):
    '''params_cycle : COMA params_1
    | empty'''

# -------- Body --------

def p_body(p):
    "body : CORCHETEIZQ statement_opt CORCHETEDER"

def p_statement_opt(p):
    '''statement_opt : statement statement_opt
    | empty'''

def p_statement(p):
    '''statement : assign
    | condition 
    | cycle
    | f_call
    | print'''

# -------- No lineales --------

def p_check_if(p):
    "check_if :"
    result = pilaO.pop()
    pilaType.pop()
    generate_quad_operator("GotoF",result,"","_")
    pilaSalto.append(quadCounter-1)

def p_fill_if(p):
    "fill_if :"
    salto = pilaSalto.pop()
    fill_goto(salto,quadCounter)
    
def p_condition(p):
    "condition : IF PARENIZQ expresion PARENDER check_if body else PUNTOCOMA fill_if"

def p_fill_else(p):
    "fill_else :"
    generate_quad_operator("Goto","","","_")
    falso = pilaSalto.pop()
    pilaSalto.append(quadCounter-1)
    fill_goto(falso,quadCounter)

def p_else(p):
    '''else : ELSE fill_else body
    | empty'''

def p_check_while(p):
    "check_while :"
    pilaSalto.append(quadCounter)

def p_fill_while(p):
    "fill_while :"
    result = pilaO.pop()
    pilaType.pop()
    verdadero = pilaSalto.pop()
    generate_quad_operator("GotoT",result,"",verdadero)

def p_cycle(p):
    "cycle : DO check_while body WHILE PARENIZQ expresion PARENDER PUNTOCOMA fill_while"

def p_f_call(p):
    "f_call : ID PARENIZQ expresion_opt PARENDER PUNTOCOMA"

# -------- Lineales --------

def p_print(p):
    "print : PRINT PARENIZQ printable PARENDER PUNTOCOMA"

def p_push_print(p):
    "push_print :"
    poper.append("print")

def p_push_string(p):
    "push_string : "
    pilaO.append(p[-1])
    pilaType.append("string")

def p_check_for_print(p):
    "check_for_print :"
    if(len(poper) > 0):
        if(poper[-1] == "print"):
            operator = poper.pop()
            der = pilaO.pop()
            pilaType.pop()
            generate_quad_operator(operator,"","",der)
        
def p_printable(p):
    '''printable : push_print CTE_STRING push_string check_for_print printable_1
    | push_print expresion check_for_print printable_1'''

def p_printable_1(p):
    '''printable_1 : COMA printable
    | empty'''

# -------- Expresiones --------

def p_push_to_pilaO(p):
    "push_to_pilaO :"
    if(p[-2] == "-"):
        if p[-1] in dirFunc[curr_func]["vars"]:
            generate_quad_operator("-",constVarTable['0']["dir"],dirFunc[curr_func]["vars"][p[-1]]["dir"],"")
        else:
            generate_quad_operator("-",constVarTable['0']["dir"],constVarTable[p[-1]]["dir"],"")
    else:
        if p[-1] in dirFunc[curr_func]["vars"]:
            pilaO.append(dirFunc[curr_func]["vars"][p[-1]]["dir"])
        else:
            pilaO.append(constVarTable[p[-1]]["dir"])

    if p[-1] in dirFunc[curr_func]["vars"]:
        pilaType.append(dirFunc[curr_func]["vars"][p[-1]]["type"])
    elif p[-1].find(".") != -1:
        pilaType.append("float")
    else:
        pilaType.append("int")

def p_push_operator(p):
    "push_operator :"
    poper.append(p[-1])

def p_check_for_assign(p):
    "check_for_assign :"
    if(len(poper) > 0):
        if(poper[-1] == "="):
            operator = poper.pop()
            der = pilaO.pop()
            izq = pilaO.pop()
            check_semantics(operator, lexer.lineno)
            generate_quad_operator(operator,der,"",izq)

def p_check_variable(p):
    "check_variable :"
    if "vars" in dirFunc[curr_func]:
        if not p[-1] in dirFunc[curr_func]["vars"]:
            raise Exception("Variable no declarada: '%s' en la línea: %d" % (p[-1], lexer.lineno))
    else:
        raise Exception("Variable no declarada: '%s' en la línea: %d" % (p[-1], lexer.lineno))

    
    p[0] = p[-1]

def p_assign(p):
    "assign : ID check_variable push_to_pilaO IGUAL push_operator expresion check_for_assign PUNTOCOMA"

def p_expresion_opt(p):
    '''expresion_opt : expresion expresion_cycle
    | empty'''

def p_expresion_cycle(p):
    '''expresion_cycle : COMA expresion_opt
    | empty'''

def p_check_for_expresion(p):
    "check_for_expresion :"
    if(len(poper) > 0):
        if(poper[-1] == ">" or poper[-1]=="<" or poper[-1] == "!="):
            operator = poper.pop()
            der = pilaO.pop()
            izq = pilaO.pop()
            check_semantics(operator, lexer.lineno)
            generate_quad_operator(operator,izq,der,"")
        
def p_expresion(p):
    "expresion : exp expresion_1"

def p_expresion_1(p):
    '''expresion_1 : MENORQUE push_operator exp check_for_expresion
    | MAYORQUE push_operator exp check_for_expresion
    | DIFERENTE push_operator exp check_for_expresion
    | empty'''

def p_check_for_plus_minus(p):
    "check_for_plus_minus :"
    if(len(poper) > 0):
        if(poper[-1] == "+" or poper[-1]=="-"):
            operator = poper.pop()
            der = pilaO.pop()
            izq = pilaO.pop()
            check_semantics(operator, lexer.lineno)
            generate_quad_operator(operator,izq,der,"")
        
def p_exp(p):
    "exp : termino check_for_plus_minus exp_1"

def p_exp_1(p):
    '''exp_1 : MINUS push_operator exp
    | PLUS push_operator exp
    | empty'''

def p_check_for_mult_div(p):
    "check_for_mult_div :"
    if(len(poper) > 0):
        if(poper[-1] == "*" or poper[-1]=="/"):
            operator = poper.pop()
            der = pilaO.pop()
            izq = pilaO.pop()
            check_semantics(operator, lexer.lineno)
            generate_quad_operator(operator,izq,der,"")
        
def p_termino(p):
    "termino : factor check_for_mult_div termino_1"

def p_termino_1(p):
    '''termino_1 : MULT push_operator termino
    | DIV push_operator termino
    | empty'''

def p_pop_par(p):
    "pop_par :"
    poper.pop()

def p_factor(p):
    '''factor : PARENIZQ push_operator expresion PARENDER pop_par
    | MINUS factor_1 push_to_pilaO
    | PLUS factor_1 push_to_pilaO
    | factor_1 push_to_pilaO'''
        
def p_factor_1(p):
    '''factor_1 : ID check_variable
    | cte'''
    p[0] = p[1]

def p_check_int(p):
    "check_int :"
    if not p[-1] in constVarTable:
        dir = get_dir("const_int")
        constVarTable[p[-1]] = {"dir":dir, "value": int(p[-1])}

def p_check_float(p):
    "check_float :"
    if not p[-1] in constVarTable:
        dir = get_dir("const_float")
        constVarTable[p[-1]] = {"dir":dir, "value": float(p[-1])}

def p_cte(p):
    '''cte : CTE_INT check_int
    | CTE_FLOAT check_float'''
    p[0] = p[1]

def p_empty(p):
    "empty :"
    pass

# Manejo de errores
def p_error(p):
    raise Exception("Error de sintaxis, se encontro elemento inesperado del tipo %s con valor: '%s' en la linea: %d " % (p.type, p.value, lexer.lineno))

parser = yacc.yacc(start="program")

while True:

    poper = []
    pilaO = []
    pilaType = []
    pilaSalto = []
    quadQueue = []
    quadCounter = 1
    tempCounter = 0
    intCounter = 0
    floatCounter = 0
    tempVarTable = {}

    try :
        input_ = int(input('''Seleccione un archivo de prueba o ingrese su propio texto en el archivo personalizado, ingrese 0 o cualquier elemento que no esté en la lista para salir:
1. test_1 (Completo) 
2. test_2 (Error léxico) 
3. test_3 (Error sintáctico)
4. test_4 (Simple)
5. test_5 (Error Semántico)
6. test_6 (Multiple declaración de parámetros)
7. test_7 (Multiple declaración de funciones)
8. test_8 (Multiple declaración de variables)
9. test_9 (Variable no declarada)
10. Custom (Coloque su texto de prueba en el archivo custom.txt)
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
            with open('test_9.txt','r') as archivo:
                s = archivo.read()
        elif(input_ == 10):
            with open('custom.txt','r') as archivo:
                s = archivo.read()
        else:
            break
        result = parser.parse(s)

    except ValueError:
        print("Entrada no válida, ingrese un número")
    except Exception as e:
        print("Error:", e)
        
    