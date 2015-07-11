import math, sys, random

def makeChains(corpus, keyLength):
    """Takes an input text as a string and returns a dictionary of
    markov chains."""
    chainDict = {}

    for line in corpus:
        for word in line:
            wordIndex = line.index(word)
            # Get the words for the next key based on the current index and the key length
            wordGroup = line[wordIndex:wordIndex+keyLength]

            if len(wordGroup) < keyLength:
                # The word selection isn't completely contained within the list, making it shorter.
                # Shift the selection back by the difference of the keyLength and the length of the
                # word and use that as the word group
                wordGroup = line[wordIndex-(keyLength-len(wordGroup)):wordIndex+keyLength-(keyLength-len(wordGroup))]
                if wordIndex + keyLength - (keyLength - len(wordGroup)) + 1 > len(line):
                    # There is no word following the selection: the line ends
                    followingWord = None
                else:
                    # Use word immediately following selection as key
                    followingWord = line[wordIndex+keyLength-(keyLength-len(wordGroup))]
            elif wordIndex + keyLength + 1 > len(line):
                # There is no word following the selection: the line ends
                followingWord = None
            else:
                # Use word immediately following selection as key
                followingWord = line[wordIndex + keyLength]

            if tuple(wordGroup) not in chainDict:
                chainDict[tuple(wordGroup)] = [followingWord]
            else:
                chainDict[tuple(wordGroup)].append(followingWord)

    return chainDict

def makeText(chains, partAmount, lineNum, emptyLines):
    """Takes a dictionary of markov chains and returns random text
    based off an original text."""
    randomText = []

    for l in range(lineNum):
        partKey = random.choice(chains.keys())
        sentenceStart = True
        sentenceEnd = False
        line = ""

        # Only add to the line if it's not empty
        if l not in emptyLines:
            for i in range(partAmount):
                for part in partKey:
                    # Add the current part to the random text
                    if sentenceStart:
                        # Capitalize the first letter in the part if it's the start of a new line
                        part = part.capitalize()
                        sentenceStart = False
                    line += part + " "

                if sentenceEnd:
                    # The previous sentence ended, so a random part to start the new line is needed
                    partKey = random.choice(chains.keys())
                    sentenceStart = True
                else:
                    # Get a random value from the dict that follows the key. The more frequent it is in
                    # the list, the more likely it is to be chosen.
                    partValue = random.choice(chains[partKey])

                if partValue == None:
                    # The part isn't followed by anything, so a random part to start the new sentence is
                    # needed
                    partKey = random.choice(chains.keys())
                    sentenceStart = True
                else:
                    # Find a key that starts with the value to add to the random text next.
                    matchingKeys = []
                    for key in chains.keys():
                        if key[0] == partValue:
                            matchingKeys.append(key)
                    if matchingKeys == []:
                        # No key starts with the value. It needs to be added to the text and then a new
                        # sentence will start
                        sentenceEnd = True
                        partKey = [partValue]
                    else:
                        # Choose a random key from the keys that begin with the value
                        partKey = random.choice(matchingKeys)
        randomText.append(line)

    return randomText

def splitIntoWordLists(corpus):
    """Remove all newline characters, split the text into
    lists of words, and remove the blank lines."""
    fileLines = corpus.split("\n")
    lineNum = len(fileLines)
    emptyLines = []
    for line in fileLines:
        lineIndex = fileLines.index(line)
        fileLines[lineIndex] = line.split(" ")
        if fileLines[lineIndex] == [""]:
            emptyLines.append(lineIndex)

    # Loop through empty line indexes in reverse order
    for lineIndex in reversed(emptyLines):
        del fileLines[lineIndex]

    return fileLines, lineNum, emptyLines

def getPartAmount(corpus, keyLength):
    """Get the amount of parts to put into the random text from the
    chain dictionary so that the random text has about the same amount
    of words as the original text"""
    sampleLine = random.choice(corpus)

    # Round up with math.ceil
    return int(math.ceil(float(len(sampleLine))/float(keyLength)))

def main():
    script, fileName = sys.argv
    fileContents = open(fileName).read()

    keyLength = 2

    # Change file into lists to count words
    inputText, lineNum, emptyLines = splitIntoWordLists(fileContents)
    for line in inputText:
        assert keyLength <= len(line), "keyLength cannot be greater than the amount of words in the shortest line"

    partAmount = getPartAmount(inputText, keyLength)
    chainDict = makeChains(inputText, keyLength)
    randomText = makeText(chainDict, partAmount, lineNum, emptyLines)
    for line in randomText:
        print line

if __name__ == "__main__":
    main()
    
