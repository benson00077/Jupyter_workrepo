# Usage
Dump translation for korean subtitles into json file, timestamp/id aligend w/ korean one.

## Prerequisite
- OS: windows
- Directories deifned in `const.py`
- Switch target translation language in `const.py`

## Input Files
Please define below:
- Merged subtitles at `../subtitles/{SHOW}/merged` in format `ko1_zh1.txt`

## Output Files
path: `../subtitles/json`

datas:
```json
[
  { chunckId: 1220, startTime: "00:58:28.625", subtitles: ["你會煮嗎？"] },
  { chunckId: 1221, startTime: "00:58:31.375", subtitles: ["我之前替她煮過"] },
  {
    chunckId: 1222,
    startTime: "00:58:32.750",
    subtitles: ["-真的嗎？", "-更重要的是"],
  },
];
```