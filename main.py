from datetime import date
import os

##TO-DO##
#Multiple fields within a deck support
#Tidy code

#Constants#
HIRAGANA = ["あ","い","う","え","お","か","き","く","け","こ","さ","し","す","せ","そ","た","ち","つ","て","と","な","に","ぬ","ね","の","は","ひ","ふ","へ","ほ","ま","み","む","め","も","ら","り","る","れ","ろ","わ","を","や","ゆ","よ","ん","が","ぎ","ぐ","げ","ご","ざ","じ","ず","ぜ","ぞ","だ","ぢ","づ","で","ど","ば","び","ぶ","べ","ぼ","ぱ","ぴ","ぷ","ぺ","ぽ","ゃ","ゅ","ょ","っ","ー"]
KATAKANA = ["ア","イ","ウ","エ","オ","カ","キ","ク","ケ","コ","サ","シ","ス","セ","ソ","タ","チ","ツ","テ","ト","ナ","ニ","ヌ","ネ","ノ","ハ","ヒ","フ","ヘ","ホ","マ","ミ","ム","メ","モ","ラ","リ","ル","レ","ロ","ワ","ヲ","ヤ","ユ","ヨ","ン","ガ","ギ","グ","ゲ","ゴ","ザ","ジ","ズ","ゼ","ゾ","ダ","ヂ","ヅ","デ","ド","バ","ビ","ブ","ベ","ボ","パ","ピ","プ","ペ","ポ","ャ","ュ","ョ","ッ","ー"]
HALFKATA = []

def katakanaToHiragana(katakanaChar):
    position = KATAKANA.index(katakanaChar)

    return HIRAGANA[position]

def isKana(char):
    if char in HIRAGANA or char in KATAKANA:
        return True
    else:
        return False

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

def checkBracketContentLocaction(field):

    bracketFound = False
    bracketStart = 0
    bracketEnd = 0

    for x in range(0, len(field)):
        if field[x] == "[":
            bracketFound = True
            bracketStart = x + 1
        if field[x] == "]":
            bracketEnd = x - 1

    return bracketFound, bracketStart, bracketEnd

def searchForKana(field, start, end):

    containsKana = False

    for x in range(start, end):
        currentChar = field[x]
        if isKana(currentChar):
            containsKana = True
            return containsKana
    
    return containsKana

def searchForComma(field, start, end):

    commaFound = False
    commaWordStart = 0

    for x in range(start, end):
        currentChar = field[x]
        if currentChar == ",":
            commaFound = True
            commaWordStart = x + 1
            return commaFound, commaWordStart
    
    return commaFound, commaWordStart

def trippleTidy(matureValue, field, furiSearchSt, furiSearchEd, wordSearchSt, wordSearchEd, edSearchSt, edSearchEd):

    furiganaField = ""
    wordField = ""
    for x in range(furiSearchSt, furiSearchEd):
        currentChar = field[x]
        if isKana(currentChar):
            if currentChar in KATAKANA:
                currentChar = katakanaToHiragana(currentChar)
            furiganaField = furiganaField + currentChar
    for y in range(wordSearchSt, wordSearchEd):
        currentChar = field[y]
        ordValue = ord(currentChar)
        if ordValue > 1000:
            wordField = wordField + currentChar
    for z in range(edSearchSt, edSearchEd):
        currentChar = field[z]
        ordValue = ord(currentChar)
        if ordValue > 1000:
            wordField = wordField + currentChar
    formattedLine = wordField + " " + furiganaField + " " + matureValue

    return formattedLine

def dupeTidy(matureValue, field):

    tidiedField = ""
    furiganaField = ""
    for x in range(0, len(field)):
        currentChar = field[x]
        if isKana(currentChar):
            tidiedField = tidiedField + currentChar
    if tidiedField[1] in KATAKANA:
        for y in range(0, len(tidiedField)):
            currentChar = tidiedField[y]
            furiganaField = furiganaField + katakanaToHiragana(currentChar)
        formattedLine = tidiedField + " " + furiganaField + " " + matureValue
        return formattedLine
    else:
        formattedLine = tidiedField + " " + tidiedField + " " + matureValue
        return formattedLine

def formatList(cleanedList):

    formattedList = []

    for x in range(0, len(cleanedList)):
        currentLine = cleanedList[x]
        splitLine = currentLine.split(" ")
        mainField = splitLine[0]
        matureValue = splitLine[1]

        #Check for []
        bracketResults = checkBracketContentLocaction(mainField)
        bracketsFound = bracketResults[0]

        if bracketsFound:
            bracketStart = bracketResults[1]
            bracketEnd = bracketResults[2]

            #Check for kana
            kanaFound = searchForKana(mainField, bracketStart, bracketEnd)
            
            if kanaFound:
                #Check for commas
                commaResults = searchForComma(mainField, bracketStart, bracketEnd)
                commaFound = commaResults[0]
                
                if commaFound:
                    commaWordStart = commaResults[1]
                    if ord(mainField[commaWordStart]) > 1000:
                        formattedLine = trippleTidy(matureValue, mainField, commaWordStart, bracketEnd, 0, bracketStart, bracketEnd, len(mainField))
                        formattedList.append(formattedLine)

                    else:
                        formattedLine = trippleTidy(matureValue, mainField, bracketStart, commaWordStart, 0, bracketStart, bracketEnd, len(mainField))
                        formattedList.append(formattedLine)

                
                else:
                    formattedLine = trippleTidy(matureValue, mainField, bracketStart, len(mainField), 0, bracketStart, bracketEnd, len(mainField))
                    formattedList.append(formattedLine)


            else:
                formattedLine = dupeTidy(matureValue, mainField)
                formattedList.append(formattedLine)
        
        else:
            formattedLine = dupeTidy(matureValue, mainField)
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
    sortedLines = orderLines(formattedLines)
    savingLine = convertToSavingFormat(sortedLines)
    writeFile("799d8d06-248a-49a3-8998-01ca54d81882.json", savingLine)

main()
