import json

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
        cuadQueue = result[2].replace("[","").replace("]","")

        cuadQueue = loadQuad(cuadQueue)
    
    return dirFunc, tabConst, cuadQueue

leer_comp_result()
