# Daniel Evaristo Escalera Bonilla - A00831289 29/05/2024
# VM.py
import json
import parser_

# Bases para la memoria
baseInt = 1000
baseFloat = 4000
baseTemp = 8000
baseConstInt = 15000
baseConstFloat = 20000

# Memoria y comandos de ejecución globales
memory = {}
quadQueue = []
quadCounter = 0

# PrepareMemory 
# O(n) donde n es la cantidad de variables más grande entr la tabla de variables y la tabla de constantes.
# Crea la estructura de memoria del programa, que consiste en un diccionario de 5 arreglos, y establece la longitud de esos arreglos.
# Inserta los valores constantes a utilizar en el arreglo correspondiente.
def prepareMemory(dirFunc, tabConst):

    varIntCount = 0
    varFloatCount = 0

    if "vars" in dirFunc["global"]:
        variables = dirFunc["global"]["vars"]

        for key in variables:
            if variables[key]["dir"] < baseFloat:
                varIntCount = max(varIntCount, variables[key]["dir"]-(baseInt-1))
            else:
                varFloatCount = max(varFloatCount, variables[key]["dir"]-(baseFloat-1))

    memory = {
        "varInt": [0]*varIntCount,
        "varFloat": [0.0]*varFloatCount,
        "temp": [],
        "constInt": [],
        "constFloat": [],
    }

    for key in tabConst:
        if tabConst[key]["dir"] < baseConstFloat:
            memory["constInt"].append(tabConst[key]["value"])
        else:
            memory["constFloat"].append(tabConst[key]["value"])

    return memory

# loadQuad
# O(n) donde n es 4 veces la cantidad de cuádruplos ya que se leee cada uno de los 4 que se encuentran en la estructura
# Recrea la fila de cuádruplos de la recibida como string en el archivo de compilación
# Busca la cantidad de variables temporales a utilizar y crea su arreglo en la memoria
def loadQuad(quadQueue, memory):
    stringArray = quadQueue.replace("\n", "").split("&")

    quadQueueArray = []

    for quad in stringArray:
        quadStringArray = quad.split(",")
        quadA = []
        for dir in quadStringArray:
            if dir == " ''" or dir == '' :
                quadA.append('')
            else:
                try:
                    quadA.append(int(dir))
                except ValueError:
                    quadA.append(dir)
        quadQueueArray.append(quadA)
    
    # Eliminar cuádruplo vacío que se genera al final
    quadQueueArray.pop()

    tempCounter = 0

    for quad in quadQueueArray:
        tempCounter = max(tempCounter, quad[3]-(baseTemp-1))

    memory["temp"] = [0]*tempCounter

    return quadQueueArray

# leer_comp_result
# Inicia el proceso de lectura del archivo de compilación
def leer_comp_result():
    with open("result.obej","r") as f:
        result = f.read().split("$")

        dirFunc = json.loads(result[0].replace("'",'"'))
        tabConst = json.loads(result[1].replace("'",'"'))

        memory = prepareMemory(dirFunc,tabConst)

        quadQueue = result[2].replace("[","").replace("]","")

        quadQueue = loadQuad(quadQueue, memory)
    
    return memory, quadQueue

# ObtenerValorOperando
# O(1)
# Recibe la dirección de un operando y regresa su valor registrado en la memoria
def obtenerValorOperando(operando):
    if operando < baseFloat:
        return memory["varInt"][operando-baseInt]
    elif operando < baseTemp:
        return memory["varFloat"][operando-baseFloat]
    elif operando < baseConstInt:
        return memory["temp"][operando-baseTemp]
    elif operando < baseConstFloat:
        return memory["constInt"][operando-baseConstInt]
    else:
        return memory["constFloat"][operando-baseConstFloat]

# ejecutarOperacion
# O(1)
# Ejecuta acciones aritméticas dependiendo del operador recibido y las almacena en el resultado
def ejecutarOperacion(operador,operando1, operando2, resultado):
    valorOperando1 = obtenerValorOperando(operando1)
    valorOperando2 = obtenerValorOperando(operando2)

    if operador == 0:
        memory["temp"][resultado-baseTemp] = valorOperando1 + valorOperando2
    if operador == 1:
        memory["temp"][resultado-baseTemp] = valorOperando1 - valorOperando2
    if operador == 2:
        memory["temp"][resultado-baseTemp] = valorOperando1 * valorOperando2
    if operador == 3:
        memory["temp"][resultado-baseTemp] = valorOperando1 / valorOperando2

# ejecutarAsignación
# O(1)
# Guarda el valor de una variable en la variable a asignar
def ejecutarAsignacion(valor, asignado):
    valor = obtenerValorOperando(valor)

    if asignado < baseFloat:
        memory["varInt"][asignado-baseInt] = valor
    elif asignado < baseTemp:
        memory["varFloat"][asignado-baseFloat] = valor
    elif asignado < baseConstInt:
        memory["temp"][asignado-baseTemp] = valor
    elif asignado < baseConstFloat:
        memory["constInt"][asignado-baseConstInt] = valor
    else:
        memory["constFloat"][asignado-baseConstFloat] = valor

# ejecutarExpresión
# O(1)
# Ejecuta acciones lógicas dependiendo del operador recibido y las almacena en el resultado
def ejecutarExpresion(operador,operando1, operando2, resultado):
    valorOperando1 = obtenerValorOperando(operando1)
    valorOperando2 = obtenerValorOperando(operando2)

    if operador == 5:
        memory["temp"][resultado-baseTemp] = int(valorOperando1 > valorOperando2)
    if operador == 6:
        memory["temp"][resultado-baseTemp] = int(valorOperando1 < valorOperando2)
    if operador == 7:
        memory["temp"][resultado-baseTemp] = int(valorOperando1 != valorOperando2)

# ejecutarPrint
# O(1)
# Despliega el valor de la dirección indicada en la consola
def ejecutarPrint(resultado):
        if isinstance(resultado,int):
            valorOperando = obtenerValorOperando(resultado)
            print(valorOperando)
        else:
            print(resultado.strip().replace('"',"").replace("'",""))

#ejecutarGoto, ejecutarGotoF, ejecutarGotoT
# O(1)
# Cambia el contador de cuádruplos para realizar las acciones desde el cuádruplo indicado
def ejecutarGoto(objetivo):
    global quadCounter
    quadCounter = objetivo-2

def ejecutarGotoF(condicion, objetivo):
    valorOperando1 = obtenerValorOperando(condicion)

    if(valorOperando1 == 0):
        global quadCounter
        quadCounter = objetivo-2

def ejecutarGotoT(condicion, objetivo):
    valorOperando1 = obtenerValorOperando(condicion)

    if(valorOperando1 == 1):
        global quadCounter
        quadCounter = objetivo-2

def executeQuad(quad):
    if quad[0] == 0 or quad[0] == 1 or quad[0] == 2 or quad[0] == 3:
        ejecutarOperacion(quad[0], quad[1], quad[2], quad[3])
    if quad[0] == 4:
        ejecutarAsignacion(quad[1], quad[3])
    if quad[0] == 5 or quad[0] == 6 or quad[0] == 7:
        ejecutarExpresion(quad[0], quad[1], quad[2], quad[3])
    if quad[0] == 8:
        ejecutarPrint(quad[1])
    if quad[0] == 9:
        ejecutarGoto(quad[3])
    if quad[0] == 10:
        ejecutarGotoF(quad[1],quad[3])
    if quad[0] == 11:
        ejecutarGotoT(quad[1],quad[3])    

# loadQuad
# O(n) donde n es la candidad de cuadrulplos obtenidos de la compilación
# Ejecuta cada cuádruplo en orden
# Busca la cantidad de variables temporales a utilizar y crea su arreglo en la memoria
def ejecutarCodigo():
    global quadCounter
    global memory
    global quadQueue
    memory, quadQueue = leer_comp_result()

    with open("Ejecucion.txt","+w") as f:
        while quadCounter < len(quadQueue):
            print("Ejecutando:",quadCounter+1,quadQueue[quadCounter], file=f)
            executeQuad(quadQueue[quadCounter])
            quadCounter = quadCounter+1
        print(memory, file=f)

archivo = input("Ingrese el nombre del archivo a compilar y ejecutar (Sin extensión):\nEjemplos: factorial, fibonacci, primos, valor_maximo\n")

try:
    parser_.compilar(archivo)
    ejecutarCodigo()
except Exception as e:
    print(e)
