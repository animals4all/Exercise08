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

def makeText(chains, partAmount):
    """Takes a dictionary of markov chains and returns random text
    based off an original text."""
    randomText = ""
    partKey = random.choice(chains.keys())
    lineStart = True
    lineEnd = False

    for i in range(partAmount):
        for part in partKey:
            # Add the current part to the random text
            if lineStart:
                # Capitalize the first letter in the part if it's the start of a new line
                part = part.capitalize()
                lineStart = False
            randomText += part + " "

        if lineEnd:
            # The previous line ended, so a random part to start the new line is needed
            partKey = random.choice(chains.keys())
            lineStart = True
        else:
            # Get a random value from the dict that follows the key. The more frequent it is in the
            # list, the more likely it is to be chosen.
            partValue = random.choice(chains[partKey])

        if partValue == None:
            # The part isn't followed by anything, so a random part to start the new line is needed
            partKey = random.choice(chains.keys())
            lineStart = True
        else:
            # Find a key that starts with the value to add to the random text next.
            matchingKeys = []
            for key in chains.keys():
                if key[0] == partValue:
                    matchingKeys.append(key)
            if matchingKeys == []:
                # No key starts with the value. It needs to be added to the text and then a new line
                # will start
                lineEnd = True
                partKey = [partValue]
            else:
                # Choose a random key from the keys that begin with the value
                partKey = random.choice(matchingKeys)

    return randomText

def splitIntoWordLists(corpus):
    """Remove all newline characters, split the text into
    lists of words, and remove the blank lines."""
    fileLines = corpus.split("\n")
    for line in fileLines:
        lineIndex = fileLines.index(line)
        fileLines[lineIndex] = line.split(" ")
        if fileLines[lineIndex] in ([], [""]):
            fileLines.remove(fileLines[lineIndex])

    return fileLines

def getPartAmount(corpus, keyLength):
    """Get the amount of parts to put into the random text from the
    chain dictionary so that the random text has about the same amount
    of words as the original text"""
    sampleLine = random.choice(corpus)

    # Round up with math.ceil
    return int(math.ceil(float(len(sampleLine))/float(keyLength)))

def main():
    #script, fileName = sys.argv
    fileContents = open("testRhyme2.txt").read()

    keyLength = 2

    # Change file into lists to count words
    inputText = splitIntoWordLists(fileContents)
    for line in inputText:
        assert keyLength <= len(line), "keyLength cannot be greater than the amount of words in the shortest line"

    partAmount = getPartAmount(inputText, keyLength)
    chainDict = makeChains(inputText, keyLength)
    randomText = makeText(chainDict, partAmount)
    print randomText

if __name__ == "__main__":
    main()
    