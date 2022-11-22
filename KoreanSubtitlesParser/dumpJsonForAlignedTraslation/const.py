import os
# Config
TARGET_LAN = 'zh'   # 你現在在執行的是 Korean 跟哪個語言 merged 的檔案?
EP_MAX_COUNT = 7    # merged 總共16集，就給 16+1
START_LINE = 15
SHOW = 'PaikSpirit'

currentDir = os.path.dirname(os.path.realpath(__file__))
parentDir = os.path.dirname(currentDir)
dataDir = parentDir + f'\\subtitles'
pathKorean = dataDir + f'\\{SHOW}\\korean'
pathMerged = dataDir + f'\\{SHOW}\\merged'
pathCopy = dataDir + f'\\{SHOW}\\copy'
pathCsv = dataDir + f'\\csv'
pathJson = dataDir + f'\\json'

def getDirectoryPaths():
    if not SHOW:
        raise RuntimeError('Must provide a SHOW name!')
    DIRS = {
        'DIR_ORIGIN': pathKorean,
        'DIR_COPY': pathCopy,
        'FILE_JSON': pathJson,
    }
    return DIRS

def getFilePaths(i:int):
    if not SHOW:
        raise RuntimeError('Must provide a SHOW name!')
    FILES = {
        'FILE_ORIGIN': pathKorean + f'\\ko{i}.txt',
        'FILE_COPY': pathCopy + f'\\ko{i}_copy.txt',
        'FILE_JSON': pathJson + f'\\{SHOW}_ko_{i}.json',
    }
    return FILES