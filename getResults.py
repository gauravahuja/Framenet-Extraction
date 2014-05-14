def getPhrase(sentence, start, end):
    phrase = sentence[start:end+1]
    i = end+1
    while i < len(sentence) and sentence[i].isalpha():
        phrase += sentence[i]
        i += 1 
    phrase = phrase.strip()
    return phrase

def getNewHead(depList, fe, headWord, headWordPOS, wc, target, phraseWords):
    if wc == 1:
        if headWordPOS == "IN":
            for (a, b, c) in depList:
                if a[0] == "prep" and a[1] == headWord and target in b[0]:
                    fe = "%s:%s" %(fe, a[1])
                    newHead = c[0]
                    return (fe, newHead)
        if headWordPOS == "DT":
            fe = "%s:%s" %(fe, "DT")
            return (fe, headWord)
        if headWordPOS == "TO":
            fe = "%s:%s" %(fe, "TO")
            return (fe, "")
    else:
        if headWordPOS == "IN":
            for (a, b, c) in depList:
                if a[0] == "prep" and a[1] == headWord and c[0] in phraseWords:
                    fe = "%s:%s" %(fe, a[1])
                    newHead = c[0]
                    return (fe, newHead)
        if headWordPOS == "DT":
            for (a, b, c) in depList:
                if a[0] == "prep" and b[0] == headWord and c[0] in phraseWords:
                    newHead = c[0]
                    return (fe, newHead)
        if headWordPOS == "TO":
            for (a, b, c) in depList:
                if a[0] == "aux" and c[0] == 'to' and b[0] in phraseWords:
                    newHead = b[0]
                    return (fe, newHead)
    return (fe, headWord)
            




def getResults(sentence, start, end, subtrees, leaves, pos, depList, fe, target):
    phrase = getPhrase(sentence, start, end)
    words = phrase.split()
    wc = len(words)

    if wc == 1:
        phraseWordPOS = ""
        headWordPOS = ""
        headWord = ""
        charcount = 0;
        diff = 1000000000;
        for item in pos:
            (w, cPos) = item
            if w == phrase:
                if(abs(start-charcount) < diff):
                    diff = abs(start-charcount)
                    phraseWordPOS = cPos            
            charcount += len(w)
        phraseWordPOS = [phraseWordPOS.strip().split('[')[0]]
        headWordPOS = phraseWordPOS[0]
        headWord = phrase 
        if (not phraseWordPOS) or (not headWordPOS) or (not headWord):
            return None
        (fe, headWord) = getNewHead(depList, fe, headWord, headWordPOS, wc, target, words)
        return (headWord, headWordPOS, phraseWordPOS, fe)
    else:
        matchIndices = []
        for i in range(0, len(subtrees)):
            stleaves = subtrees[i].leaves()
            if len(words) == len(stleaves):
                if words == stleaves:
                    matchIndices.append(i)
        if len(matchIndices) > 0:
            subtree = subtrees[matchIndices[-1]]
            head = subtree.node.split('[')[1]
            headFields = head.split('/')
            headWord = headFields[0]
            headWordPOS = headFields[-1]
            headWordPOS = headWordPOS[:-1]
            stPOS = subtree.pos()
            phraseWordPOS = []
            for (word, wordPOS) in stPOS:
                phraseWordPOS.append(wordPOS.split('[')[0])
            (fe, headWord) = getNewHead(depList, fe, headWord, headWordPOS, wc, target, words)            
            return (headWord, headWordPOS, phraseWordPOS, fe)
        return None
    return None
