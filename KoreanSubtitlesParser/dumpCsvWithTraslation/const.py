import os
# Config
TARGET_LAN = 'zh'   # 你現在在執行的是 Korean 跟哪個語言 merged 的檔案?
EP_MAX_COUNT = 7    # merged 總共16集，就給 16+1
START_LINE = 15
SHOW = 'PaikSpirit'

def getDirectoryPaths():
    if not SHOW:
        raise RuntimeError('Must provide a SHOW name!')
    DIRS = {
        'DIR_ORIGIN': os.path.abspath('.') + f'\\origin\\{SHOW}',
        'DIR_COPY': os.path.abspath('.') + f'\\copy\\{SHOW}',
        'DIR_CSV': os.path.abspath('.') + f'\\csv\\{SHOW}',
    }
    return DIRS

def getFilePaths(i:int):
    if not SHOW:
        raise RuntimeError('Must provide a SHOW name!')
    FILES = {
        'FILE_ORIGIN': os.path.abspath('.') + f'\\origin\\{SHOW}\\ko{i}_{TARGET_LAN}{i}.txt',
        'FILE_COPY': os.path.abspath('.') + f'\\copy\\{SHOW}\\ko{i}_{TARGET_LAN}{i}_copy.txt',
        'FILE_CSV': os.path.abspath('.') + f'\\csv\\{SHOW}\\ko{i}_{TARGET_LAN}{i}.csv',
    }
    return FILES