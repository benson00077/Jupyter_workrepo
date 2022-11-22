# Usage
Dump both Korean and translation language into csv file, timestamp/id aligend w/ korean one.

## Prerequisite
- OS: windows
- Directories deifned in `const.py`
- Switch target translation language in `const.py`

## Input Files
Please define below:
- Merged subtitles at `../subtitles/{SHOW}/merged` in format `ko1_zh1.txt`

## Output Files
Dump at `../subtitles/csv`

If you wanna import csv ot excel, follow below steps to prevent encoding issue:
- open new excel
- 資料 >> CSV（匯入）
- select UTF-8