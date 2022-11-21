import os, re, shutil, csv
import pprint

'''
TODO
- update script into ipynb
- update directory logic && .gitignore
- refactor file2Dict, by multiple py files
- docs for each files
'''

# Config
TARGET_LAN = 'zh'   # 你現在在執行的是 Korean 跟哪個語言 merged 的檔案?
EP_MAX_COUNT = 2    # merged 你要16集轉成 csv
START_LINE = 15 

def removeCaptionsLines(fileCopy): # clean captions lines
    with open(fileCopy, "r+", encoding="UTF-8") as f: # open file in read / write mode
        for i in range(START_LINE):
            lineCurser = f.readline()    # read the i'th line and throw it out
        text = f.read()                  # store the rest
        f.seek(0)                        # set the cursor to the top of the file
        f.write(text)               # write the data back
        f.truncate()                     # set the file size to the current size

def file2Dict(fileCopy):
    ''' OUTPUT
    '00:58:46.625': {'ko': ['아씨, 어떡하지? 가만있어 봐', '내가 이번 금요일 뭐 하냐?'],
                'zh': ['我不確定我有沒有拍攝行程']},
    '00:58:48.750': {'ko': ['안 그러면 내가 끓여주면 되는데'], 'zh': ['如果沒有，我自己煮']},
    '''
    ''' FROM below file format
    1226
    00:59:27.666 --> 00:59:28.583 position:50.00%,middle align:middle size:80.00% line:84.67%
    <c.korean><c.bg_transparent>&lrm;'어머님 생신'</c.bg_transparent></c.korean>
    <c.traditionalchinese><c.bg_transparent>&lrm;-好</c.bg_transparent></c.traditionalchinese>
    <c.traditionalchinese><c.bg_transparent>&lrm;-“媽媽的生日”</c.bg_transparent></c.traditionalchinese>
    '''
    TIME_STAMP_PATTERN = r'[0-9]{2}:[0-9]{2}:[0-9]{2}.[0-9]{3} -->'
    KR_OPEN_TAG_PATTERN = r'<c.korean><.*?>'
    KR_CLOSE_TAG_PATTERN = r'<\/.*?><\/c.korean>'
    GENERAL_OPEN_TAG_PATTERN = r'<.*?><c.*?>'
    GENERAL_CLOSE_TAG_PATTERN = r'<\/.*?><\/c.*?>'

    # cleanText = re.sub(r'<c\.korean>.*<\/c\.korean>', '', text)
    # cleanText = re.sub(r'<.*?>', '', cleanText)

    with open(fileCopy, "r", encoding="UTF-8") as f:
        lines = f.readlines()
        print("Dict accessed....")

    '''
    subtitles = 
    ["<c.korean><c.bg_transparent>&lrm;'어머님 생신'</c.bg_transparent></c.korean>",
    '<c.traditionalchinese><c.bg_transparent>&lrm;-好</c.bg_transparent></c.traditionalchinese>',
    '<c.traditionalchinese><c.bg_transparent>&lrm;-“媽媽的生日”</c.bg_transparent></c.traditionalchinese>']
    '''
    # Get lines in file
    subtitles = [[]] # the inner [] as indicator
    for line in lines:
        if re.match(TIME_STAMP_PATTERN, line):
            # e.g. 00:00:00.375 --> 00:00:03.169
            subtitles[-1].pop()
            subtitles.append([])
        else:
            # if NOT blank string
            if line.strip() :
                # e.g. 도깨비가 된단다\n , OR 3\n , OR merely \n
                #      \_ so we need rstrip to remove \n 
                sentenceTrimmed = line.rstrip('\n')
                sentenceTrimmed = re.sub(r'&lrm;', '', sentenceTrimmed)
                subtitles[-1].append(sentenceTrimmed)
    subtitles = subtitles[1:] # offset: to delete many \n\n in the begining of ko1_copy.txt

    '''
    From 00:59:27.666 --> 00:59:28.583 position:50.00%,middle align:middle size:80.00% line:84.67%
    To   00:59:27.666
    '''
    start_times = list(filter(re.compile(TIME_STAMP_PATTERN).search, lines))
    start_times = [time.split(' ')[0] for time in start_times]

    '''
    Main
    '''
    # Merge results
    if(len(subtitles) != len(start_times)):
        raise RuntimeError('Oops! sth wrong, maybe the input .txt format is not correct')
    linesDict = {} # {..., '00:59:27.666': {'ko': ["&lrm;'어머님 생신'"], 'zh': ['&lrm;-好', '&lrm;-“媽媽的生日”']},}
    for i in range(len(start_times)):
        key = start_times[i]
        subtitlesKo = []
        subtitlesTranslated = [] 
        for subtitle in subtitles[i]:
            koLine = re.match(KR_OPEN_TAG_PATTERN, subtitle)
            translateLine = re.match(GENERAL_OPEN_TAG_PATTERN, subtitle)
            if(koLine):
                trimmed = re.sub(KR_OPEN_TAG_PATTERN, '', subtitle)
                trimmed = re.sub(KR_CLOSE_TAG_PATTERN, '', trimmed)
                subtitlesKo.append(trimmed)
            elif(translateLine):
                trimmed = re.sub(GENERAL_OPEN_TAG_PATTERN, '', subtitle)
                trimmed = re.sub(GENERAL_CLOSE_TAG_PATTERN, '', trimmed)
                subtitlesTranslated.append(trimmed)
        linesDict[key] = {'ko': subtitlesKo, TARGET_LAN: subtitlesTranslated}
    return linesDict

def dict2Csv(csvPath, linesDict): # dict transfer to csv file
    # get Table for sentence
    ''' linesDict
    '00:58:46.625': {'ko': ['아씨, 어떡하지? 가만있어 봐', '내가 이번 금요일 뭐 하냐?'],
                'zh': ['我不確定我有沒有拍攝行程']},
    '00:58:48.750': {'ko': ['안 그러면 내가 끓여주면 되는데'], 'zh': ['如果沒有，我自己煮']},
    '''
    with open(csvPath, 'w', newline='', encoding='utf-8') as outputFile:
        outputWriter = csv.writer(outputFile)
        outputWriter.writerow(['chunckID', 'start_time', 'subtitles', f'subtitles_{TARGET_LAN}'])
        chunckID = 0
        for start_time, innerDict in linesDict.items():
            linesKo = None
            linesTranslated = None
            for lan, subtitles in innerDict.items():
                if (lan == 'ko'):
                    linesKo = subtitles
                elif (lan == TARGET_LAN):
                    linesTranslated = subtitles
            print(linesKo)
            print(linesTranslated)
            outputWriter.writerow([chunckID, start_time, linesKo, linesTranslated])
            chunckID += 1

def main():
    for i in range(1, EP_MAX_COUNT):
        FILE = os.path.abspath('.') + f'\\text\\merged_subs\\ko_{TARGET_LAN}\\' + f'ko{i}_{TARGET_LAN}{i}.txt'
        FILE_COPY = os.path.abspath('.') + '\\text\\merged_subs\\backup\\' + f'ko{i}_{TARGET_LAN}{i}_copy.txt'
        FILE_CSV = os.path.abspath('.') + '\\text\\merged_subs\\csv\\' + f'ko{i}_{TARGET_LAN}{i}.csv'
        
        shutil.copy(FILE, FILE_COPY)
        removeCaptionsLines(FILE_COPY)

        linesDict = file2Dict(FILE_COPY)
        dict2Csv(FILE_CSV, linesDict)


main()