import re
from helper import getSubtitles, getStartTimes

TIME_STAMP_PATTERN = r'[0-9]{2}:[0-9]{2}:[0-9]{2}.[0-9]{3} -->'
KR_OPEN_TAG_PATTERN = r'<c.korean><.*?>'
KR_CLOSE_TAG_PATTERN = r'<\/.*?><\/c.korean>'
GENERAL_OPEN_TAG_PATTERN = r'<.*?><c.*?>'
GENERAL_CLOSE_TAG_PATTERN = r'<\/.*?><\/c.*?>'

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

def file2Dict(fileCopy, transltionLanguage):
    with open(fileCopy, "r", encoding="UTF-8") as f:
        lines = f.readlines()
    subtitles = getSubtitles(lines, TIME_STAMP_PATTERN)
    start_times = getStartTimes(lines, TIME_STAMP_PATTERN)

    if(len(subtitles) != len(start_times)):
        raise RuntimeError('Oops! sth wrong, maybe the input .txt format is not correct')

    # Merge results
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
        linesDict[key] = {'ko': subtitlesKo, transltionLanguage: subtitlesTranslated}
    return linesDict