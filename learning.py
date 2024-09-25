import sys
import os.path
import json

def updateJson(target, source):
    with open(target, "w") as file:
        json.dump(source, file)

def readArguments():
    numArguments = len(sys.argv) - 1
    dictionary = "dictionary.json"
    inputFile = "" #Nothing there

    if numArguments >= 1:
        dictionary = sys.argv[1]
    if numArguments >= 2:
        inputFile = sys.argv[2]
    
    return dictionary, inputFile

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


def main():
    dictionaryFile, inputFile = readArguments()
    dictionary = loadData(dictionaryFile)

    if inputFile == "":
        while True:
            uInput = input(">> ")
            if uInput == "":
                break
            dictionary = learn(dictionary, uInput)
            updateJson(dictionaryFile,dictionary)
    else:
        ## Help
        print("Nothing There")


main()