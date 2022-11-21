import os, re, shutil, csv, json, time
from konlpy.tag import Kkma
kkma = Kkma()

# set environment variable for konply
os.environ["JAVA_HOME"] = "C:\Program Files\Java\jdk-15.0.1"


# .srt content start with line 21
startLine = 18



# /...........helper function............../

# clean captions lines
def pop(fileCopy):
    
    with open(fileCopy, "r+", encoding="UTF-8") as f: # open file in read / write mode
        for i in range(startLine):
            lineCurser = f.readline()    # read the i'th line and throw it out
        text = f.read()                  # store the rest
        cleanText = cleanTag(text)
        f.seek(0)                        # set the cursor to the top of the file
        f.write(cleanText)               # write the data back
        f.truncate()                     # set the file size to the current size

        
# parsing srt file, leave only sequence number, time stmap, and pain text
def cleanTag (text):
    ''' FROM
    1012
        01:12:53.952 --> 01:12:55.204 position:50.00%,middle align:middle size:80.00% line:84.67% 
        <c.korean><c.bg_transparent>언제 들어왔어, 삼촌?</c.bg_transparent></c.korean>
    '''
    tmpText = re.sub(r'<.*?>', '', text)
    cleanText = re.sub(r'position(.*?%){3}', '', tmpText)
    ''' TO
    1012
    01:12:53.952 --> 01:12:55.204  
    언제 들어왔어, 삼촌?
    '''
    return cleanText

# transfer to dict with koPos
def toDict(fileCopy):
    with open(fileCopy, "r", encoding="UTF-8") as f:
        lines = f.readlines()
        print("Dict accessed....")
    
    re_pattern = r'[0-9]{2}:[0-9]{2}:[0-9]{2}.[0-9]{3} -->'   # /.....  r'/d/d:/d/d:/d/d./d/d/d -->' 不能用？ ..../
    regex = re.compile(re_pattern)

    # Get start times in file
    start_times = list(filter(regex.search, lines))
    start_times = [time.split(' ')[0] for time in start_times]
    
    # Get lines in file
    subtitles = [[]]
    for sentence in lines:
        if re.match(re_pattern, sentence):
            # e.g. 00:00:00.375 --> 00:00:03.169
            subtitles[-1].pop()
            subtitles.append([])
        else:
            # if NOT blank string
            if sentence.strip() :
                # e.g. 도깨비가 된단다\n , OR 3\n , OR merely \n
                #      \_ so we need rstrip to remove \n 
                sentenceTrimmed = sentence.rstrip('\n')
                subtitles[-1].append(sentenceTrimmed)

    # offset: to delete many \n\n in the begining of ko1_copy.txt
    subtitles = subtitles[1:] 

    # Merge results
    linesDict = {start_time:line for start_time,line in zip(start_times, subtitles)}

    return linesDict

# helper fn 
def cleanSquareBreackets(string):
    re_pattern = r'\]|\['
    return re.sub(re_pattern, '', string)

# dict transfer to json file, with parsed pos / morphs
def toJsonWithPos(linesDict):
    jsonDatas = []
    lineCount = 0
    for start_time, line in linesDict.items():
        posList = []
        for sentence in line:
            #print(sentence)
            #print(type(sentence))
            trimedSentece = cleanSquareBreackets(sentence)
            pos = kkma.pos(trimedSentece, flatten=False, join=True)
            posList.append(pos)
        #pprint.pprint(posList)
        #pprint.pprint(morphsList)
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

# /..............main function............./

epNum = 17     # 共16集

timeStart = time.time()
for i in range(1, epNum):
    start = time.time()
    # file name & get a copy
    file = os.path.abspath('.') + '\\text\\origin\\' + f'ko{i}.txt'
    fileCopy = os.path.abspath('.') + '\\text\\copy\\' + f'ko{i}_copy.txt'
    fileJson = os.path.abspath('.') + '\\text\\jsonWithPos\\' + f'ko{i}.json'
    shutil.copy(file, fileCopy)
    
    # re-organized the file downloaded and get a copy
    pop(fileCopy)
    
    # access copied files
    linesDict = toDict(fileCopy)
    jsonDatas = toJsonWithPos(linesDict)
    dumpJsonFile(jsonDatas, fileJson)
    
    print(f"episode:{i} jsonWithPos is done!")
    end = time.time()
    print(f"episode consumed: {end - start} seconds")
timeEnd = time.time()
print(f"Totoal consumed: {timeEnd - timeStart} seconds")