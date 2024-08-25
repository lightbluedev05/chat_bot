import random
import pandas as pd
from unidecode import unidecode
import string
from datetime import datetime

dataFrame = pd.read_json('chatbot_data.json')

## Levenshtein Algorithm
def get_levenshtein(string1,string2):
    size_1= len(string1) + 1
    size_2= len(string2) + 1

    matrix = [[0 for n in range(size_1)] for m in range(size_2)]

    for i in range(size_2):
        matrix[i][0] = i
    for j in range(size_1):
        matrix[0][j] = j

    for i in range(1,size_2):
        for j in range(1,size_1):
            cost = 0 if string1[j-1] == string2[i-1] else 1
            
            matrix[i][j] = min(
                matrix[i-1][j]+1,
                matrix[i][j-1]+1,
                matrix[i-1][j-1] + cost)

            if i > 1 and j>1 and string1[j-1] == string2[i-2] and string1[j-2] == string2[i-1]:
                matrix[i][j] = min(matrix[i][j],matrix[i-2][j-2]+1)
        

    return matrix[size_2-1][size_1-1]
## Validate Operation
def validate_operation(input):
    
    numberList = []
    opList = []
    counter = 0
    temp_num = []

    for n in range(0,len(input)):
        if input[n].isdigit():
            counter += 1
            temp_num.append(input[n])
        else:
            if counter > 0:
                numberList.append(int("".join(temp_num)))
                temp_num.clear()
                counter = 0

            if input[n] != ' ':
                opList.append(input[n])
    numberList.append(int("".join(temp_num)))
    
    checkEquals = opList.count('=')
    validateOp = len(opList)+1==len(numberList) and checkEquals == 1


    if validateOp:
        for n in opList:
            match n:
                case '+':
                    numberList[0] += numberList[1]
                    numberList.pop(1)
                case '-':
                    numberList[0] -= numberList[1]
                    numberList.pop(1)
                case 'x' | '*':
                    numberList[0] *= numberList[1]
                    numberList.pop(1)
                case '/':
                    numberList[0] /= numberList[1]
                    numberList.pop(1)
                case '=':
                    if numberList[0] == numberList[1]:
                        print("Chatbot: La operacion es correcta!")
                        return True
                    else:
                        print("Chatbot: La operacion es erronea!")
                        return True
    else:
        return False
        



## Saludo
def obtener_saludo():
    hora_actual = datetime.now().hour
    if 5 <= hora_actual < 12:
        return "¡Buenos días!"
    elif 12 <= hora_actual < 18:
        return "¡Buenas tardes!"
    else:
        return "¡Buenas noches!"

#! Normalizar texto
def normalizar(texto):
    texto = unidecode(texto).lower().strip()
    texto = texto.translate(str.maketrans('', '', string.punctuation))
    texto = texto.replace(" ", "")
    return texto

#! Devolver valor de tag
def get_tag(user_input):

    lenghtInput = len(user_input)
    criteria = lenghtInput/5 + 1
    if lenghtInput < 4 :
        return "default"

    for tag in dataFrame.columns:
        entradas_normalizadas = [normalizar(entrada) for entrada in dataFrame[tag]["entradas"]]

        if user_input in entradas_normalizadas:
            return tag
        else:
            for entrada in entradas_normalizadas:
                ## Validate
                if abs(len(entrada)-lenghtInput) > 3 or criteria < get_levenshtein(user_input,entrada):
                    continue
                else:
                    return tag

    return "default"

#! Devolver respuesta
def get_response(tag):
    return random.choice(dataFrame[tag]['respuestas'])

#* MI MAIN
def main():
    
    print(f"{obtener_saludo()}. Bienvenido al chatbot.")
    while True:
        user_input = input("Tú: ")
        if user_input[0].isdigit() :
            if validate_operation(user_input) is False:
                response = get_response("default")
                print(f"Chatbot: {response}")

        else:
            texto_normalizado = normalizar(user_input)
            tag = get_tag(texto_normalizado)
            response = get_response(tag)
            print(f"Chatbot: {response}")
            if tag == "despedida":
                break
        
        

if __name__ == "__main__":
    main()
