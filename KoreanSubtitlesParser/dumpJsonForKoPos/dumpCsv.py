import csv, os

def dict2Csv(csvPath, linesDict, transltionLanguage): # dict transfer to csv file
    # get Table for sentence
    ''' linesDict
    '00:58:46.625': {'ko': ['아씨, 어떡하지? 가만있어 봐', '내가 이번 금요일 뭐 하냐?'],
                'zh': ['我不確定我有沒有拍攝行程']},
    '00:58:48.750': {'ko': ['안 그러면 내가 끓여주면 되는데'], 'zh': ['如果沒有，我自己煮']},
    '''
    with open(csvPath, 'w', newline='', encoding='utf-8') as outputFile:
        outputWriter = csv.writer(outputFile)
        outputWriter.writerow(['chunckID', 'start_time', 'subtitles', f'subtitles_{transltionLanguage}'])
        chunckID = 0
        for start_time, innerDict in linesDict.items():
            linesKo = None
            linesTranslated = None
            for lan, subtitles in innerDict.items():
                if (lan == 'ko'):
                    linesKo = subtitles
                elif (lan == transltionLanguage):
                    linesTranslated = subtitles
            #print(linesKo)
            #print(linesTranslated)
            outputWriter.writerow([chunckID, start_time, linesKo, linesTranslated])
            chunckID += 1
    filePath = outputFile.name
    (head, tail) = os.path.split(filePath)
    return (head, tail)