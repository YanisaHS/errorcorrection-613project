import spacy

# To run a particular portion, just comment out whichever ones you don't need

correctSubjectVerbAgreement = 0
incorrectSubjectVerbAgreement = 0
def returnsGerundSVAgreement(word):
    if word.head.tag_ != "VBG" and word.head.tag_ != "VBN":
        return word.head
    else:
        for child in word.head.children:
            if child.dep_ == "aux" or child.dep_ == "auxpass":
                if child.tag_ == "VBG" or child.tag_ == "VBN" or child.tag_ == "MD":
                    continue
                else:
                    return child
    return word.head

def modalSearchSVAgreement(word):
    for child in word.head.children:
        if child.dep_ == "aux" or child.dep_ == "auxpass":
            if child.tag_ == "MD":
                return True
    return False

def subjectVerbAgreementClausalSubject(word):
    checkForModal = modalSearchSVAgreement(word)
    if checkForModal == True:
        if word.head.tag_ == "VB" or word.head.tag_ == "VBN":
            return True
        else:
            return False
    elif checkForModal == False:
        if word.head.tag_ == "VBN" or word.head.tag_ == "VBZ":
            return True
        else:
            return False

def subjectVerbAgreementNounSubject(word):
    verbToCheck = returnsGerundSVAgreement(word)
    checkForModal = modalSearchSVAgreement(word)
    if word.text.lower() in ["you", "they", "we"]:
        if checkForModal == True:
            if verbToCheck.tag_ == "VB":
                return True
            else:
                return False
        elif verbToCheck.tag_ == "VBP" or verbToCheck.tag_ == "VB":
            return True
        elif verbToCheck.tag_ == "VBD" and verbToCheck.text != "was":
            return True
        elif verbToCheck.text == "was":
            return False
        elif verbToCheck.tag_ != "VBP":
            return False
        else:
            return False
    elif word.text.lower() in ["he", "she", "it"] or word.tag_ == "WP":
        if checkForModal == True:
            if verbToCheck.tag_ == "VB":
                return True
            else:
                return False
        elif verbToCheck.tag_ == "VBZ" or verbToCheck.tag_ == "VB":
            return True
        elif verbToCheck.tag_ == "VBD" and verbToCheck.text != "were":
            return True
        elif verbToCheck.text == "were":
            return False
        elif verbToCheck.tag_ != "VBZ" :
            return False
        else:
            return False
    elif word.text.lower() == "i":
        if checkForModal == True:
            if verbToCheck.tag_ == "VB":
                return True
            else:
                return False
        elif verbToCheck.tag_ == "VBP" or verbToCheck.tag_ == "VB":
            return True
        elif verbToCheck.tag_ == "VBD" and verbToCheck.text != "were":
            return True
        elif verbToCheck.text == "were":
            return False
        elif verbToCheck.tag_ == "VBZ":
            return False
        else:
            return False
    else:
        if word.tag_ == "NN" or word.tag_ == "NNP" or word.tag_ == "WDT" or word.text.lower() == "this" or word.text.lower() == "that":
            if checkForModal == True:
                if verbToCheck.tag_ == "VB":
                    return True
                else:
                    return False
            elif verbToCheck.tag_ == "VBZ" or verbToCheck.tag_ == "VB":
                return True
            elif verbToCheck.tag_ == "VBD" and verbToCheck.text != "were":
                return True
            elif verbToCheck.text == "were":
                return False
            elif verbToCheck.tag_ != "VBZ":
                return False
        elif word.tag_ == "NNS" or word.tag_ == "NNPS" or word.text.lower() == "these" or word.text.lower() == "those":
            if checkForModal == True:
                if verbToCheck.tag_ == "VB":
                    return True
                else:
                    return False
            elif verbToCheck.tag_ == "VBP" or verbToCheck.tag_ == "VB":
                return True
            elif verbToCheck.tag_ == "VBD" and verbToCheck.text != "was":
                return True
            elif verbToCheck.text == "was":
                return False
            elif verbToCheck.tag_ != "VBP":
                return False 
        else:
            return False

def tenseIssues(sentence):
    presentTenseVerbs = ["VB", "VBP", "VBZ"]
    pastTenseVerbs = ["VBD"]
    currentSentenceTense = []
    for word in sentence:
        if word.pos_ != "VERB":
            continue
        if word.pos_ == "VERB":
            if currentSentenceTense == []:
                if word.tag_ in presentTenseVerbs:
                    currentSentenceTense = presentTenseVerbs
                if word.tag_ in pastTenseVerbs:
                    currentSentenceTense = pastTenseVerbs
            else:
                if word.tag_ in currentSentenceTense:
                    continue
                else:
                    return False
    return True

openTextFile = open("/Users/yanisa/GoogleDrive/School/Homework - Grad School/UofA/EN 613 SLA/Research Project/WritingTextFile.txt")
nlp = spacy.load("en_core_web_sm")
textSample = nlp(openTextFile.read())

# To run + print the SV-Agreement function:
totalNumberOfPhrases = 0
makeTxtFileCorrectSVAgreement = open("/Users/yanisa/GoogleDrive/School/Homework - Grad School/UofA/EN 613 SLA/Research Project/CorrectSVAgreement.txt", "w")
makeTxtFileIncorrectSVAgreement = open("/Users/yanisa/GoogleDrive/School/Homework - Grad School/UofA/EN 613 SLA/Research Project/IncorrectSVAgreement.txt", "w")
for word in textSample:
    if (word.dep_ == "nsubj" or word.dep_ == "nsubjpass") and not word.head.dep_ == "ccomp":
        totalNumberOfPhrases = totalNumberOfPhrases + 1
        if subjectVerbAgreementNounSubject(word) == True:
            correctSubjectVerbAgreement = correctSubjectVerbAgreement + 1
            makeSubTree = word.head.subtree
            actuallyMakeSubTree = " ".join([tree.text for tree in makeSubTree])
            makeTxtFileCorrectSVAgreement.write(actuallyMakeSubTree + "\n")
        else:
            incorrectSubjectVerbAgreement = incorrectSubjectVerbAgreement + 1
            makeSubTree = word.head.subtree
            actuallyMakeSubTree = " ".join([tree.text for tree in makeSubTree])
            makeTxtFileIncorrectSVAgreement.write(actuallyMakeSubTree + "\n")
    elif word.dep_ == "csubj" and not word.head.dep_ == "ccomp":
        totalNumberOfPhrases = totalNumberOfPhrases + 1
        if subjectVerbAgreementClausalSubject(word) == True:
            correctSubjectVerbAgreement = correctSubjectVerbAgreement + 1
            makeSubTree = word.head.subtree
            actuallyMakeSubTree = " ".join([tree.text for tree in makeSubTree])
            makeTxtFileCorrectSVAgreement.write(actuallyMakeSubTree + "\n")
        else:
            incorrectSubjectVerbAgreement = incorrectSubjectVerbAgreement + 1
            makeSubTree = word.head.subtree
            actuallyMakeSubTree = " ".join([tree.text for tree in makeSubTree])
            makeTxtFileIncorrectSVAgreement.write(actuallyMakeSubTree + "\n")

print("The number of correct instances: ", correctSubjectVerbAgreement)
print("The number of incorrect instances: ", incorrectSubjectVerbAgreement)
#print("The number of total phrases is: ", totalNumberOfPhrases)

# To run & print the tense issues function - prints as two columns:
# tempCorrect = 0
# tempIncorrect = 0
# tempNumberOfPhrases = 0
# makeTxtFileCorrectTensePhrases = open("/Users/yanisa/GoogleDrive/School/Homework - Grad School/UofA/EN 613 SLA/Research Project/CorrectTensePhrases.txt", "w")
# makeTxtFileIncorrectTensePhrases = open("/Users/yanisa/GoogleDrive/School/Homework - Grad School/UofA/EN 613 SLA/Research Project/IncorrectTensePhrases.txt", "w")
# for sentence in textSample.sents:
#     tempNumberOfPhrases = tempNumberOfPhrases + 1
#     if tenseIssues(sentence) == True:
#         tempCorrect = tempCorrect + 1
#         makeTxtFileCorrectTensePhrases.write(sentence.text + "\n")
#     else:
#         tempIncorrect = tempIncorrect + 1
#         makeTxtFileIncorrectTensePhrases.write(sentence.text + "\n")

# print("Correct use of tense: ", tempCorrect)
# print("Incorrect use of tense: ", tempIncorrect)
# print("Number of phrases: ", tempNumberOfPhrases)

# To run + print the Direct Object Phrases:
# totalObjOrComp = 0
# makeTxtFileDirectObjects = open("/Users/yanisa/GoogleDrive/School/Homework - Grad School/UofA/EN 613 SLA/Research Project/DirectObjectsAndPhrases.txt", "w")
# for word in textSample:
#     if (word.dep_ == "dobj" or word.dep_ == "ccomp") and word.pos_ == "NOUN":
#         totalObjOrComp = totalObjOrComp + 1
#         makeSubTree = word.head.subtree
#         actuallyMakeSubTree = " ".join([tree.text for tree in makeSubTree])
#         print("Direct Object Phrases: ", actuallyMakeSubTree)
#         makeTxtFileDirectObjects.write(actuallyMakeSubTree + "\n")

#print(totalObjOrComp)

# Indefinite Article error identification done manually - no script needed
