import re, os

def createDir(path: str):
    if not os.path.exists(path):
        print(f'Creating {path}...')
        os.umask
        os.mkdir(path, mode=0o77)
    else:
        print(f'Directory already exist: {path}...')

def removeCaptionsLines(fileCopy: str, linesToRemove: int): # clean captions lines
    with open(fileCopy, "r+", encoding="UTF-8") as f: # open file in read / write mode
        for i in range(linesToRemove):
            lineCurser = f.readline()    # read the i'th line and throw it out
        text = f.read()                  # store the rest
        f.seek(0)                        # set the cursor to the top of the file
        f.write(text)                    # write the data back
        f.truncate()                     # set the file size to the current size

def getSubtitles(lines: list[str], timeStampPattern):
    '''
    subtitles = 
    ["<c.korean><c.bg_transparent>&lrm;'어머님 생신'</c.bg_transparent></c.korean>",
    '<c.traditionalchinese><c.bg_transparent>&lrm;-好</c.bg_transparent></c.traditionalchinese>',
    '<c.traditionalchinese><c.bg_transparent>&lrm;-“媽媽的生日”</c.bg_transparent></c.traditionalchinese>']
    '''
    # Get lines in file
    subtitles = [[]] # the inner [] as indicator
    for line in lines:
        if re.match(timeStampPattern, line):
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
    return subtitles

def getStartTimes(lines: list[str], timeStampPattern):
    '''
    From 00:59:27.666 --> 00:59:28.583 position:50.00%,middle align:middle size:80.00% line:84.67%
    To   00:59:27.666
    '''
    start_times = list(filter(re.compile(timeStampPattern).search, lines))
    start_times = [time.split(' ')[0] for time in start_times]
    return start_times

