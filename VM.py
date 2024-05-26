import json

baseInt = 1000
baseFloat = 4000
baseTemp = 8000
baseConstInt = 15000
baseConstFloat = 20000

def prepareMemory(dirFunc, tabConst):

    varIntCount = 0
    varFloatCount = 0

    variables = dirFunc["global"]["vars"]

    for key in variables:
        if variables[key]["dir"] < baseFloat:
            varIntCount = max(varIntCount, variables[key]["dir"]-(baseInt-1))
        else:
            varFloatCount = max(varFloatCount, variables[key]["dir"]-(baseFloat-1))

    memory = {
        "varInt": [0]*varIntCount,
        "varFloat": [0]*varFloatCount,
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

def loadQuad(quadQueue):
    stringArray = quadQueue.replace("\n", "").split("&")

    quadQueueArray = []

    for quad in stringArray:
        quadStringArray = quad.split(",")
        quadA = []
        for dir in quadStringArray:
            if dir == " ''" or dir == '' :
                quadA.append('')
            else:
                quadA.append(int(dir))
        quadQueueArray.append(quadA)
    
    quadQueueArray.pop()

    return quadQueueArray

def leer_comp_result():
    with open("result.txt","r") as f:
        result = f.read().split("$")

        dirFunc = json.loads(result[0].replace("'",'"'))
        tabConst = json.loads(result[1].replace("'",'"'))

        memory = prepareMemory(dirFunc,tabConst)

        quadQueue = result[2].replace("[","").replace("]","")

        quadQueue = loadQuad(quadQueue)
    
    return memory, quadQueue

def obtenerValorOperando(operando1):
    # print(memory, operando1)
    if operando1 < baseFloat:
        return memory["varInt"][operando1-baseInt]
    elif operando1 < baseTemp:
        return memory["varFloat"][operando1-baseFloat]
    elif operando1 < baseConstInt:
        return memory["temp"][operando1-baseTemp]
    elif operando1 < baseConstFloat:
        return memory["constInt"][operando1-baseConstInt]
    else:
        return memory["constFloat"][operando1-baseConstFloat]

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

def executeQuad(quad):
    if(quad[3] >= baseTemp and quad[3] < baseConstInt):
        memory["temp"].append(0)

    if quad[0] == 0 or quad[0] == 1 or quad[0] == 2 or quad[0] == 3:
        ejecutarOperacion(quad[0], quad[1], quad[2], quad[3])
    if quad[0] == 4:
        ejecutarAsignacion(quad[1], quad[3])
    

memory, quadQueue = leer_comp_result()

for quad in quadQueue:
    print(quad)
    executeQuad(quad)
    print(memory)
