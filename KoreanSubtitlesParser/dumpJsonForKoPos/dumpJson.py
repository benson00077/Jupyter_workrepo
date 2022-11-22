import os, json
import konlpy
from helper import cleanSquareBreackets

kkma = konlpy.tag.Kkma()
# set environment variable for konply
os.environ["JAVA_HOME"] = "C:\Program Files\Java\jdk-15.0.1"

def getJsonWithPos(linesDict):
    ''' linesDict
    {'00:58:57.416': ['- 아니, 얘가 좀 끓여야지', '- 아니야, 그렇지 않아'],
     '00:58:59.708': ['(석원) 음, 약속했다']}
    '''    
    jsonDatas = []
    lineCount = 0
    for start_time, line in linesDict.items():
        posList = []
        for sentence in line:
            #trimedSentece = cleanSquareBreackets(sentence)
            trimmedSentence = sentence
            pos = kkma.pos(trimmedSentence, flatten=False, join=True)
            posList.append(pos)
        jsonData = {
            'chunckId': lineCount,
            'startTime': start_time,
            'subtitles': line,
            'pos': posList,
        }
        jsonDatas.append(jsonData)
        lineCount += 1
    return jsonDatas
    
def dumpJsonFile(jsonDatas, filePath):
    with open(filePath, "w", encoding='utf8') as outfile:
        json.dump(jsonDatas, outfile, ensure_ascii=False)
    return outfile

def dict2Json(jsonPath, linesDict): # dict transfer to json file
    jsonWithPos = getJsonWithPos(linesDict)
    outfile = dumpJsonFile(jsonWithPos, jsonPath)
    filePath = outfile.name
    (head, tail) = os.path.split(filePath)
    return (head, tail)