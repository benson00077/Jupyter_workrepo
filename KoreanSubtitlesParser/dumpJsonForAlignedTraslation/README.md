# Usage
Dump korean subtitles into json file with korean pos tags.

## Prerequisite
- OS: windows
- KoNLPy and Java
- Directory, since we hav


## Output
path: `../subtitles/json`

datas:
```json
[
  {
    chunckId: 1220,
    startTime: "00:59:08.833",
    subtitles: ["뭐, 어떻게 연락을 드려야지?"],
    pos: [
      [
        ["뭐/NP", ",/SP"],
        ["어떻/VA", "게/ECD"],
        ["연락/NNG", "을/JKO"],
        ["드리/VV", "어야지/EFN", "?/SF"],
      ],
    ],
  },
  {
    chunckId: 1221,
    startTime: "00:59:10.166",
    subtitles: ["- (석원) 아냐, 이거 일단", "- (종원) 너 일단 전화번호 줘"],
    pos: [
      [
        ["-/SW"],
        ["(/SS"],
        ["석/MDN"],
        ["원/NNM", ")/SS"],
        ["알/VV", "냐/EFQ", ",/SP"],
        ["이거/NP"],
        ["일단/MAG"],
      ],
      [
        ["-/SW"],
        ["(/SS"],
        ["종/NNG"],
        ["원/NNG", ")/SS"],
        ["느/VV", "어/ECS"],
        ["일단/MAG"],
        ["전화/NNG", "번호/NNG"],
        ["주/VV", "어/ECS"],
      ],
    ],
  },
];
```