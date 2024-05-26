import json

def prepareMemory(dirFunc, tabConst):

    varIntCount = 0
    varFloatCount = 0
    constIntCount = 0
    constFloatCount = 0

    variables = dirFunc["global"]["vars"]

    for key in variables.sort:
        print(key)

    memory = {
        "varInt": [0]*4,
        "varFloat": [],
        "temp": [],
        "constInt": [],
        "constFloat": [],
    }

    print(memory)

    return memory

def loadQuad(cuadQueue):
    stringArray = cuadQueue.replace("\n", "").split("&")

    cuadQueueArray = []

    for quad in stringArray:
        quadStringArray = quad.split(",")
        quadA = []
        for dir in quadStringArray:
            if dir == " ''" or dir == '' :
                quadA.append('')
            else:
                quadA.append(int(dir))
        cuadQueueArray.append(quadA)
    
    cuadQueueArray.pop()
    
    print(cuadQueueArray)

    return cuadQueueArray

def leer_comp_result():
    with open("result.txt","r") as f:
        result = f.read().split("$")

        dirFunc = json.loads(result[0].replace("'",'"'))
        tabConst = json.loads(result[1].replace("'",'"'))

        prepareMemory(dirFunc,tabConst)

        cuadQueue = result[2].replace("[","").replace("]","")

        cuadQueue = loadQuad(cuadQueue)
    
    return dirFunc, tabConst, cuadQueue

leer_comp_result()
