import random
import pandas as pd
from unidecode import unidecode
import string
from datetime import datetime

import customtkinter as ctk
from PIL import Image
import os

import sys
import json

dataFrame = pd.read_json('chatbot_data3.json')
image = ctk.CTkImage(Image.open("logo_kevin.png"), size=(30, 30))

## FUNCIONES PARA LA GENERACION DE TEXTOOOOOOO *************************************************************

def updateJson(target, source):
    with open(target, "w") as file:
        json.dump(source, file)

def loadData(filename):
    if not os.path.exists(filename):
        with open(filename, "w") as file:
            json.dump({}, file)
    with open(filename, "r") as file:
        data = json.load(file)
    return data

def learn(file, input):
    words = input.split(" ")
    for i in range (0,len(words)-1):
        present = words[i]
        future = words[i+1]
        ## Save data to file
        if present not in file:
            file[present] = {future:1} ## New Entry
        else:
            continuesList = file[present]
            if future not in continuesList:
                file[present][future] = 1   ## New *next* Entry
            else:
                file[present][future] = file[present][future] + 1 ## Increment if already found entry
    
    return file


def mainLearning(input):

    dictionaryFile = "dictionary.json"
    inputFile = "" #Nothing there
    ##dictionaryFile, inputFile = readArguments()
    dictionary = loadData(dictionaryFile)

    dictionary = learn(dictionary,input)
    updateJson(dictionaryFile,dictionary)

    #if inputFile == "":
    #    while True:
    #        uInput = input(">> ")
    #        if uInput == "":
    #            break
    #        dictionary = learn(dictionary, uInput)
    #        updateJson(dictionaryFile,dictionary)
    #else:
    #    ## Help
    #    print("Nothing There")
    
def getNextWord(searchP, file):
    if searchP not in file:
        return list(file.keys())[random.randint(0, len(file) - 1)]
    else:
        candidates = file[searchP]
        candidatesNorm = []

        for word in candidates:
            freq = candidates[word]
            for i in range(0,freq):
                candidatesNorm.append(word)
        
        return candidatesNorm[random.randint(0,len(candidatesNorm)-1)]


def loadTData(filename):
    if not os.path.exists(filename):
        sys.exit("Error:: No dictionary.json")
    
    try:
        with open(filename, "r") as file:
            data = json.load(file)
    except json.JSONDecodeError:
        sys.exit("Error:: Invalid JSON in the file.")
    
    return data


def mainGeneration(searchParameter, length):
    file = "dictionary.json"

    dictionary = loadTData(file)

    output = ""
    for i in range(0,length):
        nextWord = getNextWord(searchParameter,dictionary)
        output = output + " " + nextWord
        searchParameter = nextWord
    
    return output


## *********************************************************************************************************


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
    if opList.count('(') > 0:
        return "default"
        
    validateOp = len(opList)+1-2*opList.count('(')==len(numberList) and checkEquals == 1


    if validateOp:
        terms = [""]
        count = 0
        countMK2 = 0
        for n in numberList:
            terms[count] = terms[count] + " " + str(n)
            if countMK2 < (len(opList)):
                if opList[countMK2] == '=':
                    count+=1
                    countMK2 +=1
                    terms.append("")
                elif opList[countMK2] == '(' or opList[countMK2] == ')':
                    while True:
                        terms[count] = terms[count] + " " + str(opList[countMK2])
                        countMK2 +=1
                        if not opList[countMK2] == '(' or opList[countMK2] == ')':
                            break
                else:
                    terms[count] = terms[count] + " " + str(opList[countMK2])
                    countMK2 +=1
                
                
        
        #print(f"{terms[0]} = {terms[1]}")


        if eval(terms[0]) == eval(terms[1]):
            return "operation_true"
        else:
            return "operation_false"



    else:
        return "default"
        
        
        


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
    if tag == "get-unique-response":
        return mainGeneration("&&&&&&&&&&",9) ## to be reworked or something


    return random.choice(dataFrame[tag]['respuestas'])

def print_response(chat_frame, chat_entry):
    user_input = chat_entry.get()
    chat_entry.delete(0, 'end')

    ## Check for number or "()"" input
    if user_input[0].isdigit() or user_input[0] == '(':
        tag = validate_operation(user_input)

    else:

        mainLearning(user_input)
        tag = "get-unique-response"
        
        #texto_normalizado = normalizar(user_input)
        #tag = get_tag(texto_normalizado)


    #texto_normalizado = normalizar(user_input)
    #tag = get_tag(texto_normalizado)
    
    if tag == "despedida":
        print("Chatbot: ¡Adiós! Que tengas un buen día.")
    
    question_frame = ctk.CTkFrame(chat_frame, fg_color="#EBEBEB")
    question_frame.pack(side="top", fill="x", padx=5, pady=(5,0))
    question_label = ctk.CTkLabel(question_frame, justify="right", corner_radius=5, wraplength=300, fg_color="#DADADA", text=user_input, font=("Arial", 12), text_color="black", anchor="e")
    question_label.pack(side="right", padx=(80,0))
    
    print(tag)
    response = get_response(tag, user_input)
    print(tag)
    
    answer_frame = ctk.CTkFrame(chat_frame, fg_color="#EBEBEB")
    answer_frame.pack(side="top", fill="x", padx=5, pady=(5,0))
    kevin_frame = ctk.CTkLabel(answer_frame, text="", image=image)
    kevin_frame.pack(side="left", padx=0)
    answer_label = ctk.CTkLabel(answer_frame, justify="left", corner_radius=5, width=300, wraplength=300, fg_color="#DADADA", text=response, font=("Arial", 12), text_color="black", anchor="w")
    answer_label.pack(side="left", padx=(5,0))
    
    chat_frame.update_idletasks()
    


#* MI MAIN
def main():
    root = ctk.CTk()
    root.geometry("500x500")
    root.resizable(False, False)
    root.title("Chatbot GPT 5.0")
    
    
    title_label = ctk.CTkLabel(root, text="Chatbot GPT 5.0", font=("Arial", 20, "bold"), text_color="white")
    title_label.pack(side="top", fill="x", pady=(20,0))
    
    chat_frame = ctk.CTkScrollableFrame(root, fg_color="#EBEBEB")
    chat_frame.pack(fill="both", expand=True, padx=40, pady=20)
    
    entry_frame = ctk.CTkFrame(root, fg_color="#232323")
    entry_frame.pack(fill="x", padx=20, pady=(0,40))
    
    chat_entry = ctk.CTkEntry(entry_frame, font=("Arial", 12),text_color="black", width=50, fg_color="#EBEBEB")
    chat_entry.pack(side="left", padx=20, fill="x", expand=True)
    
    button_entry = ctk.CTkButton(entry_frame, text="Enviar", font=("Arial", 12), command=lambda: print_response(chat_frame, chat_entry))
    button_entry.pack(side="right", padx=(0,20))
    
    chat_entry.bind("<Return>", lambda event: print_response(chat_frame, chat_entry))
    
    
    
    hello_frame = ctk.CTkFrame(chat_frame, fg_color="#EBEBEB")
    hello_frame.pack(side="top", fill="x", padx=5, pady=(5,0))
    kevin_frame = ctk.CTkLabel(hello_frame,text="", image=image)
    kevin_frame.pack(side="left", padx=0)
    hello_label = ctk.CTkLabel(hello_frame, corner_radius=5, width=300, fg_color="#DADADA", text=f"{obtener_saludo()}. Bienvenido al Chatbot GPT 5.0", font=("Arial", 12), text_color="black", anchor="w")
    hello_label.pack(side="left", padx=(5,0))
    
    root.mainloop()

if __name__ == "__main__":
    main()