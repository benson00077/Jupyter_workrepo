import re
from helper import getSubtitles, getStartTimes

TIME_STAMP_PATTERN = r'[0-9]{2}:[0-9]{2}:[0-9]{2}.[0-9]{3} -->'
KR_OPEN_TAG_PATTERN = r'<c.korean><.*?>'
KR_CLOSE_TAG_PATTERN = r'<\/.*?><\/c.korean>'
GENERAL_OPEN_TAG_PATTERN = r'<.*?><c.*?>'
GENERAL_CLOSE_TAG_PATTERN = r'<\/.*?><\/c.*?>'

''' OUTPUT
{'00:58:57.416': ['- 아니, 얘가 좀 끓여야지', '- 아니야, 그렇지 않아'],
 '00:58:59.708': ['(석원) 음, 약속했다']}
'''

''' FROM below file format
1216
00:58:57.416 --> 00:58:59.625 position:50.00%,middle align:middle size:80.00% line:79.33% 
<c.korean><c.bg_transparent>&lrm;- 아니, 얘가 좀 끓여야지</c.bg_transparent></c.korean>
<c.korean><c.bg_transparent>&lrm;- 아니야, 그렇지 않아</c.bg_transparent></c.korean>

1217
00:58:59.708 --> 00:59:02.541 position:50.00%,middle align:middle size:80.00% line:84.67% 
<c.korean><c.bg_transparent>&lrm;(석원) 음, 약속했다</c.bg_transparent></c.korean>
'''

def file2DictKoOnly(fileCopy):
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
        for subtitle in subtitles[i]:
            subtitle = re.sub(KR_OPEN_TAG_PATTERN, '', subtitle)
            trimmed = re.sub(KR_CLOSE_TAG_PATTERN, '', subtitle)
            subtitlesKo.append(trimmed)
        linesDict[key] = subtitlesKo
    return linesDict