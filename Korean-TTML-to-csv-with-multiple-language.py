import os, re, shutil, csv
import pprint

# /...........helper function............../

          
# /.....merged files looks like this..... /
'''
    01:12:53,952 --> 01:12:55,204
    <c.korean><c.bg_transparent>언제 들어왔어, 삼촌?</c.bg_transparent></c.korean>
    你何時回來的？叔叔
'''


# merged .srt content start with line 1. no captions lines to clean
startLine = 0 

# clean captions lines
def pop_forMerged(fileCopy):
    
    with open(fileCopy, "r+", encoding="UTF-8") as f: # open file in read / write mode
        for i in range(startLine):
            lineCurser = f.readline()    # read the i'th line and throw it out
        text = f.read()                  # store the rest
        cleanText = cleanTag_forMerged(text)
        f.seek(0)                        # set the cursor to the top of the file
        f.write(cleanText)               # write the data back
        f.truncate()                     # set the file size to the current size
        
        
# parsing srt file, leave only sequence number, time stmap, and pain text
# FOR MERGED: clean the Korean context 
def cleanTag_forMerged (text):
    #cleanText = re.sub(r'<c.korean>.*?</c.korean>\n', '', text)
    cleanText = re.sub(r'<.*?>', '', text)
    # &lrm 是故意留的， 爲了讓之後 excel 内 雙語好分開 
    #cleanText = re.sub(r'&lrm;', '', cleanText)
    # \n 都取代掉，toDict() would return empty {}
    #cleanText = re.sub(r'\n', '', cleanText)
    return cleanText





# transfer to dict
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
            subtitles[-1].pop()
            subtitles.append([])
        else:
            subtitles[-1].append(sentence)
    subtitles = subtitles[1:]         

    # Merge results
    linesDict = {start_time:line for start_time,line in zip(start_times, subtitles)}
    # pprint.pprint(linesDict)
    return linesDict


# dict transfer to csv file
def toCsv(csvPath, linesDict, language):
    
    # get Table for sentence
    with open(sentenceCsv, 'w', newline='', encoding='utf-8') as outputFile:
        outputWriter = csv.writer(outputFile)
        outputWriter.writerow(['chunckID', 'start_time', f'subtitles_{language}'])
        chunckID = 0
        for start_time, line in linesDict.items():
            outputWriter.writerow([chunckID, start_time, line])
            chunckID += 1




# /..............main function............./

target_lan = 'zh' # 你現在在執行的是 Korean 跟哪個語言 merged 的檔案?
epNum = 2        # merged 你要16集轉成 csv

for i in range(1, epNum):
    
    # file name & get a copy
    file = os.path.abspath('.') + f'\\text\\merged_subs\\ko_{target_lan}\\' + f'ko{i}_{target_lan}{i}.txt'
    fileCopy = os.path.abspath('.') + '\\text\\merged_subs\\backup\\' + f'ko{i}_{target_lan}{i}_copy.txt'
    shutil.copy(file, fileCopy)
    
    # access copied files
    pop_forMerged(fileCopy)
    linesDict = toDict(fileCopy)
    
    # csv for Sentence Table
    sentenceCsv = os.path.abspath('.') + '\\text\\merged_subs\\csv\\' + f'ko{i}_{target_lan}{i}.csv'
    toCsv(sentenceCsv, linesDict, target_lan)

    print(f"episode:{i} csv for merged subtitles -- Ko & {target_lan} is done!")