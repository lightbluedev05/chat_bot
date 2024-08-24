import random
import pandas as pd
from unidecode import unidecode
import string
from datetime import datetime

import customtkinter as ctk
from PIL import Image
import os

dataFrame = pd.read_json('chatbot_data.json')
kevin_image = ctk.CTkImage(Image.open("logo_kevin.png"), size=(30, 30))

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

def print_response(chat_frame, chat_entry):
    user_input = chat_entry.get()
    chat_entry.delete(0, 'end')
    texto_normalizado = normalizar(user_input)
    tag = get_tag(texto_normalizado)
    
    if tag == "despedida":
        print("Chatbot: ¡Adiós! Que tengas un buen día.")
    
    question_frame = ctk.CTkFrame(chat_frame, fg_color="#EBEBEB")
    question_frame.pack(side="top", fill="x", padx=5, pady=(5,0))
    question_label = ctk.CTkLabel(question_frame, justify="right", corner_radius=5, wraplength=300, fg_color="#DADADA", text=user_input, font=("Arial", 12), text_color="black", anchor="e")
    question_label.pack(side="right", padx=(80,0))
    
    response = get_response(tag)
    
    answer_frame = ctk.CTkFrame(chat_frame, fg_color="#EBEBEB")
    answer_frame.pack(side="top", fill="x", padx=5, pady=(5,0))
    kevin_frame = ctk.CTkLabel(answer_frame, text="", image=kevin_image)
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
    
    
    
    hello_frame = ctk.CTkFrame(chat_frame, fg_color="#EBEBEB")
    hello_frame.pack(side="top", fill="x", padx=5, pady=(5,0))
    kevin_frame = ctk.CTkLabel(hello_frame,text="", image=kevin_image)
    kevin_frame.pack(side="left", padx=0)
    hello_label = ctk.CTkLabel(hello_frame, corner_radius=5, width=300, fg_color="#DADADA", text=f"{obtener_saludo()}. Bienvenido al Chatbot GPT 5.0", font=("Arial", 12), text_color="black", anchor="w")
    hello_label.pack(side="left", padx=(5,0))
    
    root.mainloop()
    
    
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