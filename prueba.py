import re
from sympy import symbols, Eq, solve 

preposiciones = []


add_preposiciones = True

print("Chatbot: Hola, soy Kevin, un chatbot de proposiciones")

while (add_preposiciones):
    print("Chatbot: Inserte una proposicion por favor")
    preposicion = input("Usuario: ")
    preposiciones.append(preposicion)
    print("Chatbot: ¿Desea insertar otra proposicion?")
    if(input("Usuario: ") == "no"):
        add_preposiciones = False

patterns = {
    "es par" : r"(\w+)\s(es par)",
    "es menor que": r"(\w+)\s(es menor que)\s(\d+)",
    "es mayor que": r"(\w+)\s(es mayor que)\s(\d+)",
}

def separar_proposicion(prop):
    for key, pattern in patterns.items():
        match = re.match(pattern, prop)
        if match:
            return [match.groups(), key]

    return None

def analizar_proposiciones(proposiciones_separadas):
    variables = {}
    resultados = []
    
    for prop, key in proposiciones_separadas:
        var = prop[0]
        
        # Crear símbolo en SymPy si no existe
        if var not in variables:
            variables[var] = symbols(var)
        
        if key == "es par":
            # Crear ecuación simbólica
            eq = Eq(variables[var] % 2, 0)
        elif key == "es menor que":
            eq = variables[var] < int(prop[2])
        elif key == "es mayor que":
            eq = variables[var] > int(prop[2])
        
        resultados.append(eq)
    
    # Resolver las proposiciones en conjunto
    soluciones = solve(resultados, list(variables.values()))
    return soluciones

proposiciones_separadas = [separar_proposicion(prop) for prop in preposiciones]
soluciones = analizar_proposiciones(proposiciones_separadas)

print(preposiciones)
print(proposiciones_separadas)
print(soluciones)

