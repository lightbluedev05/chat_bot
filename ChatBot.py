import random
import pandas as pd
from unidecode import unidecode
import string
from datetime import datetime

dataFrame = pd.read_json('chatbot_data.json')

<<<<<<< Updated upstream
=======
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
## Find OP character
def isOperator(char):
    search = set('+x*-/=()')
    if char in search:
        return True
    else:
        return False

## Validate Operation
def validate_operation(input):
    input=input.replace(" ","")
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

            if input[n] != ' ' and isOperator(input[n]):
                opList.append(input[n])
            else:
                return "default"
    numberList.append(int("".join(temp_num)))
    
    checkEquals = opList.count('=')
    validateOp = len(opList)+1-2*opList.count('(')==len(numberList) and checkEquals == 1


    if validateOp:
        terms = [""]
        count = 0
        countMK2 = 0
        for n in numberList:
            terms[count] = terms[count] + " " + str(n)
            if countMK2 < (len(numberList)-1):
                if opList[countMK2] == '=':
                    count+=1
                    terms.append("")
                else:
                    terms[count] = terms[count] + " " + str(opList[countMK2])
            countMK2 +=1

        if eval(terms[0]) == eval(terms[1]):
            return "operation_true"
        else:
            return "operation_false"

    else:
        return "default"
        
        



## Saludo
>>>>>>> Stashed changes
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
    for tag in dataFrame.columns:
        entradas_normalizadas = [normalizar(entrada) for entrada in dataFrame[tag]["entradas"]]
        if user_input in entradas_normalizadas:
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
        texto_normalizado = normalizar(user_input)
        tag = get_tag(texto_normalizado)
        
        if tag == "despedida":
            print("Chatbot: ¡Adiós! Que tengas un buen día.")
            break
        
        response = get_response(tag)
        print(f"Chatbot: {response}")

if __name__ == "__main__":
    main()