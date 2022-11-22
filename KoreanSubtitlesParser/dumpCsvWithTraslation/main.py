import shutil
from const import TARGET_LAN, EP_MAX_COUNT, START_LINE, SHOW, getFilePaths, getDirectoryPaths
from helper import removeCaptionsLines, createDir
from parseLines import file2Dict
from dumpCsv import dict2Csv

def main():
    dirPaths = getDirectoryPaths()

    for key in dirPaths:
        createDir(dirPaths[key])

    for i in range(1, EP_MAX_COUNT):
        filePaths = getFilePaths(i)

        shutil.copy(filePaths['FILE_ORIGIN'], filePaths['FILE_COPY'])
        removeCaptionsLines(filePaths['FILE_COPY'], START_LINE)

        linesDict = file2Dict(filePaths['FILE_COPY'], TARGET_LAN)
        (outputDir, outputFile) = dict2Csv(filePaths['FILE_CSV'], linesDict, TARGET_LAN)
        print(f'{outputFile} created at {outputDir} for {SHOW} with translation {TARGET_LAN}')

if __name__ == '__main__':
    main()
