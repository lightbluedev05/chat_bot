import random
import pandas as pd
from unidecode import unidecode
import string
from datetime import datetime

dataFrame = pd.read_json('chatbot_data.json')

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