import sys
import os.path
import json
import random

def readArguments():
    leng = 50
    filename = "dictionary.json"

    numArgs = len(sys.argv) - 1
    if numArgs >= 1:
        leng = int(sys.argv[1])
    if numArgs >= 2:
        filename = sys.argv[2]
    return leng,filename
    
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


def loadData(filename):
    if not os.path.exists(filename):
        sys.exit("Error:: No dictionary.json")
    
    try:
        with open(filename, "r") as file:
            data = json.load(file)
    except json.JSONDecodeError:
        sys.exit("Error:: Invalid JSON in the file.")
    
    return data


def main():
    length, file = readArguments()
    dictionary = loadData(file)

    searchParameter = "$$$$$$$$$$$$$"
    output = ""
    for i in range(0,length):
        nextWord = getNextWord(searchParameter,dictionary)
        output = output + " " + nextWord
        searchParameter = nextWord
    
    print(output)

main()