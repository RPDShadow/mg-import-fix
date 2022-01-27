from datetime import date
import os

##TO-DO##
#Multiple fields within a deck support
#Katakana to hiragana conversion

def findFiles():
    txtFiles = []
    for file in os.listdir(os.getcwd()):
        if file.endswith(".txt"):
            txtFiles.append(os.path.join(os.getcwd(), file))
    return txtFiles

def selectFromList(listName, passedList):
    print("\n" + listName + " list. Please enter a number to select desired file, or enter 'a' to select all.\n")
    for num in range(0, len(passedList)):
        print(str(num)+": "+passedList[num])
    listSelection = input("\nEnter selection: ")
    if listSelection == "a":
        userSelection = passedList
    else:
        userSelection = []
        listSelection = int(listSelection)
        userValue = passedList[listSelection]
        userSelection.append(userValue)

    return userSelection

def getDecks(fileName):
    deckNames = []
    currentFile = open(fileName, encoding="utf-8")
    currentContents = currentFile.read().splitlines()
    for x in range(0, len(currentContents)):
        currentLine = currentContents[x]
        if "deck:" in currentLine:
            inList = False
            for y in range(0, len(deckNames)):
                if currentLine == deckNames [y]:
                    inList = True
            if not inList:
                deckNames.append(currentLine)
    
    return deckNames


def findFields(fileName, deckList):
    fieldNames = {}
    fStart = 0
    fEnd = 0
    currentFile = open(fileName, encoding="utf-8")
    currentContents = currentFile.read().splitlines()
    for deckNum in range(0, len(deckList)):
        currentDeck = deckList[deckNum]
        fieldsInDeck = []
        for x in range(0, len(currentContents)):
            currentLine = currentContents[x]
            if "<--FLDSTART-->" in currentLine and currentContents[x-4] == currentDeck:
                if fStart == 0:
                    fStart = x
            if "<--FLDEND-->" in currentLine and fStart != 0:
                if fEnd == 0:
                    fEnd = x
        for y in range(fStart, fEnd):
            currentLine = currentContents[y]
            if "<<<<field:" in currentLine:
                fieldsInDeck.append(currentLine)
                fStart = 0
                fEnd = 0
        fieldNames[currentDeck] = fieldsInDeck

    print(fieldNames)

    return fieldNames

def cleanFile(fileName, fieldNames):
    newLines = []
    currentFile = open(fileName, encoding="utf-8")
    currentContents = currentFile.read().splitlines()
    for x in range(0, len(currentContents)):
        currentLine = currentContents[x]
        if "history:" in currentLine:
            currentLastReview = currentLine[-10:]
            clrList = currentLastReview.split("-")
            clrDate = date(int(clrList[0]), int(clrList[1]), int(clrList[2]))
        if "forecast:" in currentLine:
            currentForcast = currentLine[-10:]
            cfList = currentForcast.split("-")
            cfDate = date(int(cfList[0]), int(cfList[1]), int(cfList[2]))
        if "deck:" in currentLine:
            deckFields = fieldNames[currentLine]
        if "<<<<field:" in currentLine:
            for fieldNumber in range(0, len(deckFields)):
                if deckFields[fieldNumber] in currentLine:
                    currentField = currentContents[x+1]
                    dateDelta = cfDate - clrDate
                    interval = dateDelta.days
                    if interval >= 21:
                        mature = "2"
                    else:
                        mature = "1"
                    newLine = currentField + " " + mature
                    newLines.append(newLine)

    return newLines

def formatList(cleanedList):

    formattedList = []

    for x in range(0, len(cleanedList)):
        currentLine = cleanedList[x]
        splitLine = currentLine.split(" ")
        mainField = splitLine[0]
        matureValue = splitLine[1]

        #Check for []
        for y in range(0, len(mainField)):
            if mainField[y] == "[":
                bracketsFound = True
                bracketStart = y + 1
                for z in range(bracketStart, len(mainField)):
                    if mainField[z] == "]":
                        bracketEnd = z - 1
                break
            else:
                bracketsFound = False

        if bracketsFound:
            #Check for kana
            for b in range(bracketStart, bracketEnd):
                currentChar = mainField[b]
                ordValue = ord(currentChar)
                if ordValue > 10000:
                    kanaFound = True
                    break
                else:
                    kanaFound = False
            
            
            if kanaFound:
                #Check for commas
                for d in range(bracketStart, bracketEnd):
                    currentChar = mainField[d]
                    ordValue = ord(currentChar)
                    if ordValue == 44:
                        commaFound = True
                        commaWordStart = d + 1
                        break
                    else:
                        commaFound = False
                
                if commaFound:
                    furiganaField = ""
                    wordField = ""
                    untidiedField = mainField
                    if ord(untidiedField[commaWordStart]) > 1000:
                        for h in range(commaWordStart, bracketEnd):
                            currentChar = untidiedField[h]
                            ordValue = ord(currentChar)
                            if ordValue > 10000:
                                furiganaField = furiganaField + currentChar
                        for i in range(0, bracketStart):
                            currentChar = untidiedField[i]
                            ordValue = ord(currentChar)
                            if ordValue > 1000:
                                wordField = wordField + currentChar
                        for j in range(bracketEnd, len(untidiedField)):
                            currentChar = untidiedField[j]
                            ordValue = ord(currentChar)
                            if ordValue > 1000:
                                wordField = wordField + currentChar
                        formattedLine = wordField + " " + furiganaField + " " + matureValue
                        formattedList.append(formattedLine)

                    else:
                        for k in range(bracketStart, commaWordStart):
                            currentChar = untidiedField[k]
                            ordValue = ord(currentChar)
                            if ordValue > 10000:
                                furiganaField = furiganaField + currentChar
                        for l in range(0, bracketStart):
                            currentChar = untidiedField[l]
                            ordValue = ord(currentChar)
                            if ordValue > 1000:
                                wordField = wordField + currentChar
                        for m in range(bracketEnd, len(untidiedField)):
                            currentChar = untidiedField[m]
                            ordValue = ord(currentChar)
                            if ordValue > 1000:
                                wordField = wordField + currentChar
                        formattedLine = wordField + " " + furiganaField + " " + matureValue
                        formattedList.append(formattedLine)

                
                else:
                    furiganaField = ""
                    wordField = ""
                    untidiedField = mainField
                    for e in range(bracketStart, len(untidiedField)):
                        currentChar = untidiedField[e]
                        ordValue = ord(currentChar)
                        if ordValue > 10000:
                            furiganaField = furiganaField + currentChar
                    for f in range(0, bracketStart):
                        currentChar = untidiedField[f]
                        ordValue = ord(currentChar)
                        if ordValue > 1000:
                            wordField = wordField + currentChar
                    for g in range(bracketEnd, len(untidiedField)):
                        currentChar = untidiedField[g]
                        ordValue = ord(currentChar)
                        if ordValue > 1000:
                            wordField = wordField + currentChar
                    formattedLine = wordField + " " + furiganaField + " " + matureValue
                    formattedList.append(formattedLine)


            else:
                tidiedField = ""
                untidiedField = mainField
                for c in range(0, len(untidiedField)):
                    currentChar = untidiedField[c]
                    ordValue = ord(currentChar)
                    if ordValue > 10000:
                        tidiedField = tidiedField + currentChar
                formattedLine = tidiedField + " " + tidiedField + " " + matureValue
                formattedList.append(formattedLine)
        
        else:
            tidiedField = ""
            untidiedField = mainField
            for a in range(0, len(untidiedField)):
                currentChar = untidiedField[a]
                ordValue = ord(currentChar)
                if ordValue > 10000:
                    tidiedField = tidiedField + currentChar
            formattedLine = tidiedField + " " + tidiedField + " " + matureValue
            formattedList.append(formattedLine)

    return formattedList

def orderLines(unorderedLines):
    orderedLines = sorted(unorderedLines)
    
    return orderedLines

def convertToSavingFormat(wordLines):
    convertedLines = "["
    for x in range(0,len(wordLines)):
        currentLine = wordLines[x]
        splitLine = currentLine.split(" ")
        currentWord = splitLine[0]
        currentFurigana = splitLine[1]
        currentLearingStatus = int(splitLine[2])
        combinedJP = currentWord + "◴" + currentFurigana
        wordInfo = '["' + combinedJP + '",' + str(currentLearingStatus) + '],'
        convertedLines = convertedLines + wordInfo
    stringLength = len(convertedLines)
    convertedLines = convertedLines[:stringLength-1] + "]"

    return convertedLines



def writeFile(fileName, content):
    currentFile = open(fileName, encoding="utf-8", mode="a")
    currentFile.write(content)
    currentFile.close()

def main():
    files = findFiles()
    fileSelection = selectFromList("File", files)

    cleanedLines = []
    for fileNum in range(0, len(fileSelection)):
        deckSelection = {}
        fieldSelection = {}
        currentFile = fileSelection[fileNum]
        decks = getDecks(currentFile)
        deckListName = str(currentFile) + " Deck "
        deckSelection[currentFile] = selectFromList(deckListName, decks)
        fields = findFields(currentFile, deckSelection[currentFile])
        for deckNum in range(0, len(deckSelection[currentFile])):
            currentDeckFields = []
            fieldListName = str((deckSelection[currentFile])[deckNum]) + " Field "
            currentDeck = (deckSelection[currentFile])[deckNum]
            currentDeckFields = currentDeckFields + selectFromList(fieldListName, fields[currentDeck])
            fieldSelection[currentDeck] = currentDeckFields
        cleanedLines = cleanedLines + cleanFile(currentFile, fieldSelection)
    formattedLines = formatList(cleanedLines)
    writeFile("test.txt", str(formattedLines))
    sortedLines = orderLines(formattedLines)
    savingLine = convertToSavingFormat(sortedLines)
    writeFile("799d8d06-248a-49a3-8998-01ca54d81882.json", savingLine)

main()
