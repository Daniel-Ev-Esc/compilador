import json

def leer_comp_result():
    with open("result.txt","r") as f:
        result = f.read().split("$")

        return result[0].replace("'",'"'), result[1].replace("'",'"'), result[2]
    

dirFunc, tabConst, cuadQueue = leer_comp_result()

dirFunc = json.loads(dirFunc)

print("directorio", dirFunc)
# print("constantes", tabConst)
# print("cuadruplos", cuadQueue)
