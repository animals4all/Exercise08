import math, sys, random

def makeChains(corpus, keyLength):
    """Takes an input text as a string and returns a dictionary of
    markov chains."""
    chainDict = {}
    fileLines = splitIntoWordLists(corpus)

    for line in fileLines:
        if line == "":
            continue

        for word in line:
            wordIndex = line.index(word)
            wordGroup = line[wordIndex:wordIndex+keyLength]

            if len(wordGroup) < keyLength:
                wordGroup = line[wordIndex-(keyLength-len(wordGroup)):wordIndex+keyLength-(keyLength-len(wordGroup))]
                if wordIndex+keyLength-(keyLength-len(wordGroup)) + 1 > len(line):
                    followingWord = None
                else:
                    followingWord = line[wordIndex+keyLength-(keyLength-len(wordGroup))]
            elif wordIndex + keyLength + 1 > len(line):
                followingWord = None
            else:
                followingWord = line[wordIndex + keyLength]

            if tuple(wordGroup) not in chainDict:
                    chainDict[tuple(wordGroup)] = [followingWord]
            else:
                chainDict[tuple(wordGroup)].append(followingWord)

    return chainDict

def makeText(chains, partAmount):
    """Takes a dictionary of markov chains and returns random text
    based off an original text."""
    randomText = ""
    partKey = random.choice(chains.keys())
    lineStart = True
    lineEnd = False

    for i in range(partAmount):
        for part in partKey:
            if lineStart:
                part = part.capitalize()
                lineStart = False
            randomText += part + " "

        if lineEnd:
            partKey = random.choice(chains.keys())
            lineStart = True
        else:
            partValue = random.choice(chains[partKey])

        if partValue == None or lineEnd == True:
            partKey = random.choice(chains.keys())
            lineStart = True
        else:
            matchingKeys = []
            for key in chains.keys():
                if key[0] == partValue:
                    matchingKeys.append(key)
            if matchingKeys == []:
                lineEnd = True
                partKey = [partValue]
            else:
                partKey = random.choice(matchingKeys)

    return randomText

def splitIntoWordLists(corpus):
    fileLines = corpus.split("\n")
    for line in fileLines:
        lineIndex = fileLines.index(line)
        fileLines[lineIndex] = line.split(" ")

    return fileLines

def getPartAmount(corpus, keyLength):
    """Get the amount of parts to put into the random text from the
    chain dictionary."""
    fileLines = splitIntoWordLists(corpus)
    line = random.choice(fileLines)
    for line in fileLines:
        assert keyLength <= len(line), "keyLength cannot be greater than the amount of words in the longest line"

    return int(math.ceil(float(len(line))/float(keyLength)))

def main():
    script, fileName = sys.argv

    inputText = open(fileName).read()

    keyLength = 2
    partAmount = getPartAmount(inputText, keyLength)

    chainDict = makeChains(inputText, keyLength)
    print chainDict
    randomText = makeText(chainDict, partAmount)
    print randomText

if __name__ == "__main__":
    main()
    