import shutil
from const import TARGET_LAN, EP_MAX_COUNT, START_LINE, SHOW, getFilePaths, getDirectoryPaths
from helper import removeCaptionsLines, createDir
from parseLines import file2DictKoOnly
from dumpJson import dict2Json

def main():
    dirPaths = getDirectoryPaths()

    for key in dirPaths:
        createDir(dirPaths[key])

    for i in range(1, EP_MAX_COUNT):
        filePaths = getFilePaths(i)

        shutil.copy(filePaths['FILE_ORIGIN'], filePaths['FILE_COPY'])
        removeCaptionsLines(filePaths['FILE_COPY'], START_LINE)

        linesDict = file2DictKoOnly(filePaths['FILE_COPY'])
        (outputDir, outputFile) = dict2Json(filePaths['FILE_JSON'], linesDict)
        print(f'{outputFile} created at {outputDir} for {SHOW} with pos')

if __name__ == '__main__':
    main()
